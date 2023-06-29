"""启动脚本"""
import yaml
from Job import Job

if __name__ == '__main__':
    with open('config/config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    job = Job(config['required_course_teacher'],
              config['required_course_type'],
              config['cookies'],
              config['server'],
              config['prefer_sleep_range'],
              config['sleep_range'])
    job.run()
