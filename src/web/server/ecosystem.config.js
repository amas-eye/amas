module.exports = {
    /**
     * Application configuration section
     * http://pm2.keymetrics.io/docs/usage/application-declaration/
     * pm2部署工具配置
     */
    apps: [

        // First application
        {
            name: 'node_app', //应用名
            script: './bin/www.js', //启动脚本路径
            cwd: './', // 指定该app工作(项目)目录，这样pm2会相对这个目录去找脚本之类的及监听
            watch: true, //监听变化(目录或true、false)
            exec_mode: "cluster", // 部署模式node集群模式
            max_memory_restart: "512M", // 超过多少内存重启
            autorestart: true, //异常是否自动重启
            min_uptime: 60000, //应用运行少于时间被认为是异常启动
            max_restarts: 10, // 最大异常重启次数，即小于min_uptime运行时间重启次数
            restart_delay: 0, // 异常后等待多长重启时间
            instances: 4, //实例数
            ignore_watch: [
                "node_modules",
                "logs",
                "public",
                "test"
            ], //忽略监听的目录
            log_date_format: 'YYYY-MM-DD HH:mm Z', //日志时间格式
            error_file: './logs/pm_err.log', //错误日志输出位置
            out_file: './logs/pm_com.log', //普通日志输出位置
            combine_logs: true, //设置日志信息是否添加node进程pid （true不添加）
            env: {
                NODE_ENV: "development", //默认环境 
                COMMON_VARIABLE: 'true'
            },
            env_production: { //产品环境
                NODE_ENV: 'production'
            }
        },

        // Second application

        {
            name: 'node_test', //应用名
            script: './bin/www.js', //启动脚本路径
            cwd: './', // 指定该app工作(项目)目录，这样pm2会相对这个目录去找脚本之类的及监听
            watch: true, //监听变化(目录或true、false)
            exec_mode: "cluster", // 部署模式node集群模式
            max_memory_restart: "128M", // 超过多少内存重启
            autorestart: true, //异常是否自动重启
            min_uptime: 60000, //应用运行少于时间被认为是异常启动
            max_restarts: 3, // 最大异常重启次数，即小于min_uptime运行时间重启次数
            restart_delay: 0, // 异常后等待多长重启时间
            instances: 1, //实例数
            ignore_watch: [
                "node_modules",
                "logs",
                "public",
                "test"
            ], //忽略监听的目录
            log_date_format: 'YYYY-MM-DD HH:mm Z', //日志时间格式
            error_file: './logs/pm_err.log', //错误日志输出位置
            out_file: './logs/pm_com.log', //普通日志输出位置
            combine_logs: true, //设置日志信息是否添加node进程pid （true不添加）
            env: {
                NODE_ENV: "development", //默认环境 
                COMMON_VARIABLE: 'true'
            }
        }

    ],

    /**
     * Deployment section
     * http://pm2.keymetrics.io/docs/usage/deployment/
     */
    deploy: { //远程部署配置
        production: {
            user: 'node',
            host: '212.83.163.1', //主机地址
            ref: 'origin/master', // git代码分支
            repo: 'git@github.com:repo.git', //git地址
            path: '/var/www/production', //部署路径
            "ssh_options": "StrictHostKeyChecking=no", //ssh配置
            "pre-setup": "apt-get install git", // 安装项目前安装git 
            "post-setup": "ls -la", // 安装完打印目录
            "pre-deploy-local": "echo 'This is a local executed command'", //
            'post-deploy': 'npm install && pm2 startOrRestart ecosystem.config.js --env production', // 安装一来看以及 用pm2重新加载   
            env: {
                NODE_ENV: "production"
            }
        },
        dev: {
            user: 'node',
            host: '212.83.163.1',
            ref: 'origin/master',
            repo: 'git@github.com:repo.git',
            path: '/var/www/development',
            'post-deploy': 'npm install && pm2 reload ecosystem.config.js --env dev',
            env: {
                NODE_ENV: 'dev'
            }
        }
    }
};