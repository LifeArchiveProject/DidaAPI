"""任务导出服务"""
import io
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd
from utils import app_logger
from services.dida_service import dida_service
from services.pomodoro_service import pomodoro_service
from core import urls


class ExportService:
    """任务导出服务类"""
    
    def __init__(self):
        self.dida_service = dida_service
    
    async def export_tasks_to_excel(self) -> Dict[str, Any]:
        """
        导出所有任务到Excel文件
        
        Returns:
            dict: 包含Excel文件内容和元数据的响应
        """
        try:
            app_logger.info("开始导出任务到Excel")
            
            # 获取所有任务数据
            all_tasks_data = await self._get_all_tasks_data()
            completed_tasks_data = await self._get_completed_tasks_data()
            abandoned_tasks_data = await self._get_abandoned_tasks_data()
            trash_tasks_data = await self._get_trash_tasks_data()

            if not all_tasks_data and not completed_tasks_data and not abandoned_tasks_data and not trash_tasks_data:
                return {"error": "无法获取任务数据"}
            
            # 创建Excel文件
            excel_buffer = io.BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # 处理全部任务
                if all_tasks_data:
                    all_tasks_df = self._process_all_tasks(all_tasks_data)
                    if not all_tasks_df.empty:
                        all_tasks_df.to_excel(writer, sheet_name='全部任务', index=False)
                        app_logger.info(f"全部任务工作表创建完成，共 {len(all_tasks_df)} 条记录")
                
                # 处理已完成任务
                if completed_tasks_data:
                    completed_tasks_df = self._process_completed_tasks(completed_tasks_data)
                    if not completed_tasks_df.empty:
                        completed_tasks_df.to_excel(writer, sheet_name='已完成任务', index=False)
                        app_logger.info(f"已完成任务工作表创建完成，共 {len(completed_tasks_df)} 条记录")

                # 处理放弃任务
                if abandoned_tasks_data:
                    abandoned_tasks_df = self._process_abandoned_tasks(abandoned_tasks_data)
                    if not abandoned_tasks_df.empty:
                        abandoned_tasks_df.to_excel(writer, sheet_name='放弃任务', index=False)
                        app_logger.info(f"放弃任务工作表创建完成，共 {len(abandoned_tasks_df)} 条记录")

                # 处理垃圾桶任务
                if trash_tasks_data:
                    trash_tasks_df = self._process_trash_tasks(trash_tasks_data)
                    if not trash_tasks_df.empty:
                        trash_tasks_df.to_excel(writer, sheet_name='垃圾桶任务', index=False)
                        app_logger.info(f"垃圾桶任务工作表创建完成，共 {len(trash_tasks_df)} 条记录")
            
            excel_buffer.seek(0)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"滴答清单任务导出_{timestamp}.xlsx"
            
            app_logger.info(f"Excel文件生成完成: {filename}")
            
            return {
                "filename": filename,
                "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "content": excel_buffer.getvalue(),
                "size": len(excel_buffer.getvalue())
            }
            
        except Exception as e:
            app_logger.error(f"导出任务到Excel时发生错误: {e}")
            return {"error": str(e)}

    async def export_focus_records_to_excel(self) -> Dict[str, Any]:
        """
        导出专注记录到Excel文件

        Returns:
            dict: 包含Excel文件内容和元数据的响应
        """
        try:
            app_logger.info("开始导出专注记录到Excel")

            # 获取专注记录数据
            focus_timeline_data = await self._get_all_focus_timeline_data()

            if not focus_timeline_data:
                return {"error": "无法获取专注记录数据"}

            # 创建Excel文件
            excel_buffer = io.BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # 处理专注记录时间线
                if focus_timeline_data:
                    focus_timeline_df = self._process_focus_timeline(focus_timeline_data)
                    if not focus_timeline_df.empty:
                        focus_timeline_df.to_excel(writer, sheet_name='专注记录时间线', index=False)
                        app_logger.info(f"专注记录时间线工作表创建完成，共 {len(focus_timeline_df)} 条记录")

            excel_buffer.seek(0)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"滴答清单专注记录导出_{timestamp}.xlsx"

            app_logger.info(f"专注记录Excel文件生成完成: {filename}")

            return {
                "filename": filename,
                "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "content": excel_buffer.getvalue(),
                "size": len(excel_buffer.getvalue())
            }

        except Exception as e:
            app_logger.error(f"导出专注记录到Excel时发生错误: {e}")
            return {"error": str(e)}
    
    async def _get_all_tasks_data(self) -> Optional[Dict]:
        """获取所有任务数据"""
        try:
            result = await self.dida_service.get_all_tasks()
            if result and 'error' not in result:
                return result
            return None
        except Exception as e:
            app_logger.error(f"获取所有任务数据失败: {e}")
            return None
    
    async def _get_completed_tasks_data(self) -> Optional[List]:
        """获取已完成任务数据（分页获取所有数据）"""
        try:
            all_completed_tasks = []
            to = None
            page_count = 0

            while True:
                app_logger.info(f"获取已完成任务第 {page_count + 1} 页，to参数: {to}")

                result = await self.dida_service.get_completed_tasks(to, "Completed")
                if not result or 'error' in result:
                    app_logger.warning(f"获取已完成任务第 {page_count + 1} 页失败: {result}")
                    break

                if isinstance(result, list) and len(result) > 0:
                    all_completed_tasks.extend(result)
                    app_logger.info(f"第 {page_count + 1} 页获取到 {len(result)} 条已完成任务")

                    # 获取最后一个任务的completedTime作为下次分页参数
                    last_task = result[-1]
                    to = last_task.get('completedTime')
                    if not to:
                        app_logger.info("最后一个任务没有completedTime，停止分页")
                        break

                    page_count += 1

                    # 如果返回的任务数少于50条，说明已经是最后一页
                    if len(result) < 50:
                        app_logger.info("已获取到最后一页已完成任务")
                        break
                else:
                    app_logger.info("没有更多已完成任务数据")
                    break

            app_logger.info(f"已完成任务分页获取完成，共获取 {len(all_completed_tasks)} 条记录，分 {page_count} 页")
            return all_completed_tasks if all_completed_tasks else None

        except Exception as e:
            app_logger.error(f"获取已完成任务数据失败: {e}")
            return None

    async def _get_abandoned_tasks_data(self) -> Optional[List]:
        """获取放弃任务数据（分页获取所有数据）"""
        try:
            all_abandoned_tasks = []
            to = None
            page_count = 0

            while True:
                app_logger.info(f"获取放弃任务第 {page_count + 1} 页，to参数: {to}")

                result = await self.dida_service.get_completed_tasks(to, "Abandoned")
                if not result or 'error' in result:
                    app_logger.warning(f"获取放弃任务第 {page_count + 1} 页失败: {result}")
                    break

                if isinstance(result, list) and len(result) > 0:
                    all_abandoned_tasks.extend(result)
                    app_logger.info(f"第 {page_count + 1} 页获取到 {len(result)} 条放弃任务")

                    # 获取最后一个任务的completedTime作为下次分页参数
                    last_task = result[-1]
                    to = last_task.get('completedTime')
                    if not to:
                        app_logger.info("最后一个任务没有completedTime，停止分页")
                        break

                    page_count += 1

                    # 如果返回的任务数少于50条，说明已经是最后一页
                    if len(result) < 50:
                        app_logger.info("已获取到最后一页放弃任务")
                        break
                else:
                    app_logger.info("没有更多放弃任务数据")
                    break

            app_logger.info(f"放弃任务分页获取完成，共获取 {len(all_abandoned_tasks)} 条记录，分 {page_count} 页")
            return all_abandoned_tasks if all_abandoned_tasks else None

        except Exception as e:
            app_logger.error(f"获取放弃任务数据失败: {e}")
            return None
    
    async def _get_trash_tasks_data(self) -> Optional[Dict]:
        """获取垃圾桶任务数据"""
        try:
            result = await self.dida_service.get_trash_tasks()
            if result and 'error' not in result:
                return result
            return None
        except Exception as e:
            app_logger.error(f"获取垃圾桶任务数据失败: {e}")
            return None

    async def _get_all_focus_timeline_data(self) -> Optional[List]:
        """获取所有专注记录时间线数据（分页获取所有数据）"""
        try:
            all_focus_records = []
            to_timestamp = None
            page_count = 0
            max_pages = 100  # 防止无限循环

            # 获取认证信息
            current_session = self.dida_service.current_session
            if not current_session:
                app_logger.error("未找到认证会话")
                return None

            auth_token = current_session['auth_token']
            csrf_token = current_session['csrf_token']

            while page_count < max_pages:
                app_logger.info(f"获取专注记录第 {page_count + 1} 页，to_timestamp: {to_timestamp}")

                result = await pomodoro_service.get_focus_timeline(auth_token, csrf_token, to_timestamp)
                if not result or 'error' in result:
                    app_logger.warning(f"获取专注记录第 {page_count + 1} 页失败: {result}")
                    break

                # 检查是否有数据
                if not isinstance(result, list) or len(result) == 0:
                    app_logger.info("没有更多专注记录数据")
                    break

                all_focus_records.extend(result)
                app_logger.info(f"第 {page_count + 1} 页获取到 {len(result)} 条专注记录")

                # 获取最后一条记录的startTime作为下次分页参数
                if len(result) > 0:
                    last_record = result[-1]
                    start_time = last_record.get('startTime')
                    if start_time:
                        # 转换时间格式用于下次请求
                        to_timestamp = pomodoro_service._convert_time_to_timestamp(start_time)
                    else:
                        app_logger.info("最后一条记录没有startTime，停止分页")
                        break
                else:
                    break

                page_count += 1

                # 如果返回的记录数少于31条（通常每页31条），说明已经是最后一页
                if len(result) < 31:
                    app_logger.info("已获取到最后一页专注记录")
                    break

            app_logger.info(f"专注记录分页获取完成，共获取 {len(all_focus_records)} 条记录，分 {page_count} 页")
            return all_focus_records if all_focus_records else None

        except Exception as e:
            app_logger.error(f"获取专注记录时间线数据失败: {e}")
            return None
    
    def _process_all_tasks(self, data: Dict) -> pd.DataFrame:
        """处理全部任务数据"""
        try:
            tasks = data.get('syncTaskBean', {}).get('update', [])
            projects = {p['id']: p['name'] for p in data.get('projectProfiles', [])}
            
            processed_tasks = []
            for task in tasks:
                processed_task = self._flatten_task(task, projects)
                processed_tasks.append(processed_task)
            
            return pd.DataFrame(processed_tasks)
            
        except Exception as e:
            app_logger.error(f"处理全部任务数据失败: {e}")
            return pd.DataFrame()
    
    def _process_completed_tasks(self, data: List) -> pd.DataFrame:
        """处理已完成任务数据"""
        try:
            processed_tasks = []
            for task in data:
                processed_task = self._flatten_task(task, {})
                processed_tasks.append(processed_task)

            return pd.DataFrame(processed_tasks)

        except Exception as e:
            app_logger.error(f"处理已完成任务数据失败: {e}")
            return pd.DataFrame()

    def _process_abandoned_tasks(self, data: List) -> pd.DataFrame:
        """处理放弃任务数据"""
        try:
            processed_tasks = []
            for task in data:
                processed_task = self._flatten_task(task, {})
                processed_tasks.append(processed_task)

            return pd.DataFrame(processed_tasks)

        except Exception as e:
            app_logger.error(f"处理放弃任务数据失败: {e}")
            return pd.DataFrame()

    def _process_trash_tasks(self, data: Dict) -> pd.DataFrame:
        """处理垃圾桶任务数据"""
        try:
            tasks = data.get('tasks', [])

            processed_tasks = []
            for task in tasks:
                processed_task = self._flatten_task(task, {})
                processed_tasks.append(processed_task)

            return pd.DataFrame(processed_tasks)

        except Exception as e:
            app_logger.error(f"处理垃圾桶任务数据失败: {e}")
            return pd.DataFrame()

    def _process_focus_timeline(self, data: List) -> pd.DataFrame:
        """处理专注记录时间线数据 - 紧凑型展示"""
        try:
            processed_records = []
            for record in data:
                # 为每个专注会话创建一条紧凑记录
                compact_record = self._create_compact_focus_record(record)
                processed_records.append(compact_record)

            return pd.DataFrame(processed_records)

        except Exception as e:
            app_logger.error(f"处理专注记录时间线数据失败: {e}")
            return pd.DataFrame()
    
    def _flatten_task(self, task: Dict, projects: Dict) -> Dict:
        """展平任务数据，包含所有字段"""
        try:
            flattened = {
                # 基本信息
                '任务ID': task.get('id', ''),
                '任务标题': task.get('title', ''),
                '任务内容': task.get('content', ''),
                '任务描述': task.get('desc', ''),
                '项目ID': task.get('projectId', ''),
                '项目名称': projects.get(task.get('projectId', ''), ''),
                '排序顺序': task.get('sortOrder', 0),
                
                # 状态和优先级
                '任务状态': self._get_status_text(task.get('status', 0)),
                '状态代码': task.get('status', 0),
                '优先级': task.get('priority', 0),
                '完成进度': task.get('progress', 0),
                '删除状态': task.get('deleted', 0),
                
                # 时间相关
                '创建时间': task.get('createdTime', ''),
                '修改时间': task.get('modifiedTime', ''),
                '开始日期': task.get('startDate', ''),
                '截止日期': task.get('dueDate', ''),
                '置顶时间': task.get('pinnedTime', ''),
                '完成时间': task.get('completedTime', ''),
                '删除时间': task.get('deletedTime', ''),
                
                # 时区和时间设置
                '时区': task.get('timeZone', ''),
                '是否浮动时间': task.get('isFloating', False),
                '是否全天任务': task.get('isAllDay', False),
                
                # 重复设置
                '重复任务ID': task.get('repeatTaskId', ''),
                '重复标志': task.get('repeatFlag', ''),
                '重复来源': task.get('repeatFrom', ''),
                '首次重复日期': task.get('repeatFirstDate', ''),
                
                # 提醒设置
                '提醒设置': task.get('reminder', ''),
                '提醒列表': str(task.get('reminders', [])),
                '排除日期': str(task.get('exDate', [])),
                
                # 层级关系
                '父任务ID': task.get('parentId', ''),
                '子任务ID列表': str(task.get('childIds', [])),
                
                # 其他属性
                '标签列表': str(task.get('tags', [])),
                '子项目': str(task.get('items', [])),
                '附件数量': len(task.get('attachments', [])),
                '评论数量': task.get('commentCount', 0),
                '列ID': task.get('columnId', ''),
                '类型': task.get('kind', ''),
                '图片模式': task.get('imgMode', 0),
                
                # 创建者和删除者
                '创建者ID': task.get('creator', 0),
                '删除者ID': task.get('deletedBy', 0),
                
                # 版本控制
                '实体标签': task.get('etag', ''),
                
                # 专注相关
                '番茄钟摘要': str(task.get('pomodoroSummaries', [])),
                '专注摘要': str(task.get('focusSummaries', [])),
                
                # 附件详情
                '附件详情': str(task.get('attachments', [])),
            }
            
            return flattened
            
        except Exception as e:
            app_logger.error(f"展平任务数据失败: {e}")
            return {}
    
    def _get_status_text(self, status_code: int) -> str:
        """获取状态文本描述"""
        status_map = {
            0: '未完成',
            1: '进行中',
            2: '已完成',
            -1: '已删除'
        }
        return status_map.get(status_code, f'未知状态({status_code})')

    def _create_compact_focus_record(self, record: Dict) -> Dict:
        """创建紧凑型专注记录"""
        try:
            from datetime import datetime, timedelta

            # 基本信息
            session_id = record.get('id', '')
            session_start = record.get('startTime', '')
            session_end = record.get('endTime', '')
            pause_duration = record.get('pauseDuration', 0)

            # 计算总时长
            total_duration = 0
            if session_start and session_end:
                try:
                    start_time = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                    end_time = datetime.fromisoformat(session_end.replace('Z', '+00:00'))
                    total_duration = int((end_time - start_time).total_seconds())
                except:
                    total_duration = 0

            # 获取任务信息
            tasks = record.get('tasks', [])
            task_titles = []
            project_names = []

            for task in tasks:
                if task.get('title'):
                    task_titles.append(task['title'])
                if task.get('projectName'):
                    project_names.append(task['projectName'])

            main_task = '; '.join(set(task_titles))  # 去重
            main_project = '; '.join(set(project_names))  # 去重

            # 生成专注时间段描述
            focus_timeline = self._generate_focus_timeline(tasks, pause_duration)

            # 生成暂停模式描述
            pause_pattern = self._generate_pause_pattern(tasks, pause_duration)

            # 格式化会话时间
            session_time_str = ""
            if session_start and session_end:
                try:
                    start_dt = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                    end_dt = datetime.fromisoformat(session_end.replace('Z', '+00:00'))
                    session_time_str = f"{start_dt.strftime('%Y-%m-%d %H:%M')} - {end_dt.strftime('%H:%M')}"
                except:
                    session_time_str = f"{session_start} - {session_end}"

            return {
                '会话ID': session_id,
                '会话时间': session_time_str,
                '总时长': self._format_duration(total_duration),
                '暂停时长': self._format_duration(pause_duration),
                '任务标题': main_task,
                '项目': main_project,
                '专注时间段': focus_timeline,
                '暂停模式': pause_pattern,
                '效率(%)': round((total_duration - pause_duration) / total_duration * 100, 1) if total_duration > 0 else 0,
                '时间段数量': len(tasks),
                '会话类型': record.get('type', ''),
                '实体标签': record.get('etag', '')
            }

        except Exception as e:
            app_logger.error(f"创建紧凑型专注记录失败: {e}")
            return {}

    def _generate_focus_timeline(self, tasks: List[Dict], total_pause_duration: int) -> str:
        """生成专注时间段描述"""
        try:
            from datetime import datetime

            if not tasks:
                return "无专注时间段"

            timeline_parts = []

            for i, task in enumerate(tasks):
                start_time = task.get('startTime', '')
                end_time = task.get('endTime', '')

                if start_time and end_time:
                    try:
                        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                        duration = int((end_dt - start_dt).total_seconds())

                        # 格式化时间段
                        time_part = f"{start_dt.strftime('%H:%M')}-{end_dt.strftime('%H:%M')}({self._format_duration(duration)})"
                        timeline_parts.append(time_part)

                        # 如果不是最后一个时间段，计算暂停时间
                        if i < len(tasks) - 1:
                            next_task = tasks[i + 1]
                            next_start = next_task.get('startTime', '')
                            if next_start:
                                try:
                                    next_start_dt = datetime.fromisoformat(next_start.replace('Z', '+00:00'))
                                    pause_duration = int((next_start_dt - end_dt).total_seconds())
                                    if pause_duration > 0:
                                        timeline_parts.append(f"[暂停{self._format_duration(pause_duration)}]")
                                except:
                                    timeline_parts.append("[暂停未知时长]")
                    except:
                        timeline_parts.append(f"时间段{i+1}(解析失败)")

            return " → ".join(timeline_parts)

        except Exception as e:
            app_logger.error(f"生成专注时间段描述失败: {e}")
            return "生成失败"

    def _generate_pause_pattern(self, tasks: List[Dict], total_pause_duration: int) -> str:
        """生成暂停模式描述"""
        try:
            if len(tasks) <= 1:
                return "无暂停" if total_pause_duration == 0 else f"总暂停{self._format_duration(total_pause_duration)}"

            pause_count = len(tasks) - 1
            avg_pause = total_pause_duration // pause_count if pause_count > 0 else 0

            if pause_count == 1:
                return f"暂停1次({self._format_duration(total_pause_duration)})"
            else:
                return f"暂停{pause_count}次(总计{self._format_duration(total_pause_duration)}, 平均{self._format_duration(avg_pause)})"

        except Exception as e:
            app_logger.error(f"生成暂停模式描述失败: {e}")
            return "分析失败"

    def _format_duration(self, seconds: int) -> str:
        """格式化时长显示"""
        try:
            if seconds < 60:
                return f"{seconds}秒"
            elif seconds < 3600:
                minutes = seconds // 60
                remaining_seconds = seconds % 60
                if remaining_seconds == 0:
                    return f"{minutes}分钟"
                else:
                    return f"{minutes}分{remaining_seconds}秒"
            else:
                hours = seconds // 3600
                remaining_minutes = (seconds % 3600) // 60
                if remaining_minutes == 0:
                    return f"{hours}小时"
                else:
                    return f"{hours}小时{remaining_minutes}分钟"
        except:
            return f"{seconds}秒"


# 创建全局实例
export_service = ExportService()
