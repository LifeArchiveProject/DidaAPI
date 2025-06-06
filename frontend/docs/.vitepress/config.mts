import { defineConfig } from 'vitepress'

export default defineConfig({
  title: '滴答清单API文档',
  description: '滴答清单API接口文档',
  lang: 'zh-CN',

  head: [
    ['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }],
    ['meta', { name: 'theme-color', content: '#007bff' }]
  ],

  themeConfig: {
    logo: '/logo.png',

    nav: [
      { text: '首页', link: '/' },
      { text: 'API文档', link: '/api/' },
      { text: '项目地址', link: 'https://github.com/your-repo' }
    ],

    sidebar: {
      '/api/': [
        {
          text: '📖 API概览',
          collapsed: false,
          items: [
            { text: 'API文档首页', link: '/api/' },
            { text: 'URL管理', link: '/api/url-management' }
          ]
        },
        {
          text: '🔐 认证相关',
          collapsed: false,
          items: [
            { text: '认证概览', link: '/api/auth/' },
            { text: '密码登录', link: '/api/auth/password-login' },
            { text: '微信登录流程', link: '/api/auth/wechat-login-flow' },
            { text: '获取微信二维码', link: '/api/auth/get-wechat-qrcode' },
            { text: '轮询登录状态', link: '/api/auth/poll-login-status' },
            { text: '验证微信登录', link: '/api/auth/validate-wechat-login' }
          ]
        },
        {
          text: '📋 任务管理',
          collapsed: false,
          items: [
            { text: '获取所有任务', link: '/api/tasks/get-all-tasks' },
            { text: '获取已完成任务', link: '/api/tasks/get-completed-tasks' },
            { text: '获取垃圾桶任务', link: '/api/tasks/get-trash-tasks' }
          ]
        },
        {
          text: '📝 清单管理',
          collapsed: false,
          items: [
            { text: '获取清单列表', link: '/api/projects' }
          ]
        },
        {
          text: '📊 统计分析',
          collapsed: false,
          items: [
            { text: '获取用户排名统计', link: '/api/statistics' }
          ]
        },
        {
          text: '🍅 番茄专注',
          collapsed: false,
          items: [
            { text: '获取番茄专注概览', link: '/api/pomodoros' }
          ]
        },
        {
          text: '⏱️ 正计时专注',
          collapsed: false,
          items: [
            { text: '获取专注记录时间线', link: '/api/pomodoros/focus-timeline' },
            { text: '获取专注详情分布', link: '/api/pomodoros/focus-distribution' },
            { text: '获取专注趋势热力图', link: '/api/pomodoros/focus-heatmap' },
            { text: '获取专注时间按小时分布', link: '/api/pomodoros/focus-hour-distribution' },
            { text: '获取专注时间分布', link: '/api/pomodoros/focus-time-distribution' }
          ]
        },
        {
          text: '🎯 习惯管理',
          collapsed: false,
          items: [
            { text: '获取所有习惯', link: '/api/habits' },
            { text: '导出习惯数据', link: '/api/habits/export-habits' }
          ]
        },
        {
          text: '👤 用户信息',
          collapsed: false,
          items: [
            { text: '获取用户信息', link: '/api/users' }
          ]
        },
        {
          text: '🔧 自定义接口',
          collapsed: false,
          items: [
            { text: '导出任务到Excel', link: '/api/custom/export-tasks-excel' },
            { text: '导出专注记录到Excel', link: '/api/custom/export-focus-excel' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/your-repo' }
    ],



    search: {
      provider: 'local',
      options: {
        locales: {
          zh: {
            translations: {
              button: {
                buttonText: '搜索文档',
                buttonAriaLabel: '搜索文档'
              },
              modal: {
                noResultsText: '无法找到相关结果',
                resetButtonTitle: '清除查询条件',
                footer: {
                  selectText: '选择',
                  navigateText: '切换'
                }
              }
            }
          }
        }
      }
    },

    outline: {
      level: [2, 3],
      label: '页面导航'
    },

    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'medium'
      }
    }
  },

  markdown: {
    lineNumbers: true,
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    }
  }
})
