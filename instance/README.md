### Purpose of Instance Directory:
---

- For the sake of this startup template, the instance directory is considered in version control, But keep in mind that according to the [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/config/#instance-folders:~:text=The%20instance%20folder%20is%20designed%20to%20not%20be%20under%20version%20control%20and%20be%20deployment%20specific.%20It%E2%80%99s%20the%20perfect%20place%20to%20drop%20things%20that%20either%20change%20at%20runtime%20or%20configuration%20files.), this directory is meant to be private. Thus, you should remove comment for instance directory from `.gitignore` file. 
