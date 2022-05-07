# student_registion
实现hit哈尔滨工业大学每日上报（需如实上报）
submit_actions.py为搭配github actions使用的版本
# yml文件格式
在该目录下新建'submit.yml',yml文件格式如下:
```yaml
- username: "'111'"
  password: "'111'"
  address: "'111'"
- username: "'222'"
  password: "'222'"
  address: "'222'"
```
# github actions设置
submit_actions.py为github actions版本
命令执行格式为：`python ./submit_actions.py ${{ secrets.USER_USERNAME }} ${{ secrets.USER_PASSWORD }} "'黑龙江省哈尔滨市南岗区'"`
* secrets.USER_USERNAME：为学号
* secrets.USER_PASSWORD：为用户密码
