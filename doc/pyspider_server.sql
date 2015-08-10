

CREATE TABLE `tasks` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL COMMENT '任务名称',
    `start_cmd` VARCHAR(200) NULL DEFAULT NULL COMMENT '启动命令或者启动类 Ex: weibo.py weibo.xml',
    `caption` VARCHAR(50) NULL DEFAULT NULL COMMENT '任务说明',
    `config_path` VARCHAR(100) NULL DEFAULT NULL COMMENT '配置路径',
    `files` TEXT NULL COMMENT '所有外挂文件的路径',
    `create_user` VARCHAR(50) NOT NULL COMMENT '创建者',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `client_create_id` INT(11) NOT NULL DEFAULT '0' COMMENT '指定哪台客户端上传的任务',
    `end_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '上次修改时间',
    `end_client_id` INT(11) NOT NULL DEFAULT '0' COMMENT '客户端完成编号',
    `state` INT(11) NOT NULL DEFAULT '0' COMMENT '任务状态 0未分配，1被认领，10已完成，-1取消',
    `parent_task_id` INT(11) NOT NULL DEFAULT '0' COMMENT '任务的父任务编号 用0表示大任务，拆分的子任务继承自大任务。如有子任务分解，继承子任务编号即可。',
    `children_task_count` INT(11) NOT NULL DEFAULT '0' COMMENT '子任务数量',
    `client_get_id` INT(11) NOT NULL DEFAULT '0' COMMENT '指定哪台客户端获取了任务',
    `client_get_time` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '客户端获取任务的时间',
    `table_name` VARCHAR(20) NOT NULL COMMENT '数据存储哪张表',
    `table_sql` TEXT NOT NULL COMMENT '建表的sql',
    `done_number` INT(20) NOT NULL DEFAULT '0' COMMENT '完成量',
    `error_number` INT(20) NOT NULL DEFAULT '0' COMMENT '错误量',
    `retry_number` INT(20) NOT NULL DEFAULT '0' COMMENT '重试数量',
    `all_number` INT(20) NOT NULL DEFAULT '0' COMMENT '预计总量',
    `expect_end_time` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '预计完成时间',
    PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
AUTO_INCREMENT=1;



CREATE TABLE `clients` (
    `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '客户端编号',
    `name` VARCHAR(20) NOT NULL COMMENT '客户端名称',
    `state` INT(11) NOT NULL DEFAULT '0' COMMENT '客户端状态 -1删除 0=未审核 1=可用',
    `login` INT(11) NOT NULL DEFAULT '0' COMMENT '登录状态 - 0未登录  1已登录',
    `last_time` TIMESTAMP NULL DEFAULT NULL COMMENT '最后登录时间',
    `create_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `cpu` INT(11) NOT NULL DEFAULT '0' COMMENT 'CPU使用率',
    `mem_us` INT(11) NOT NULL DEFAULT '0' COMMENT '内存使用MB',
    `mem_all` INT(11) NOT NULL DEFAULT '0' COMMENT '内存大小MB',
    `speed_rx` INT(11) NOT NULL DEFAULT '0' COMMENT '下载网速KB',
    `speed_expect` INT(11) NOT NULL DEFAULT '0' COMMENT '预计网速KB',
    `driver_us` INT(11) NOT NULL DEFAULT '0' COMMENT '硬盘使用MB',
    `driver_all` INT(11) NOT NULL DEFAULT '0' COMMENT '银盘大小MB',
    PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
AUTO_INCREMENT=1;

