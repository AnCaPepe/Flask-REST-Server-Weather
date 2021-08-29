# Flask-REST-Server-Weather
Weather Buddy server implementation 

***
## Manual Execution
***
### Dependencies
***

To run the server locally, have a **Python 3.x** interpreter installed and add the necessary packages with the terminal command:

```shell
pip install -r requirements.txt
```

For the client, install the dependencies with **npm**:
```shell
npm install
```

***
### Environment
***

Before starting the application, hava a **PostgreSQL** database available and configured according to `settings.py` defaults or corresponding environment variable overrides

Initialize the database tables by executing the preconfigured migrations:

```shell
flask db upgrade
```

Then it's possible to run the web server itself, optionally defining the database host address with _DB_HOST_ (defaults to **'localhost'**), with the command:

```shell
DB_HOST=<your_host> FLASK_APP=manage.py FLASK_ENV={production,development} flask run
```

If everything is properly set up, it will be possible to call the WebAPI with **Postman** on `http://<DB_HOST>:5000`.

The client can be run with the command:
```shell
npm run serve
```

Becoming available on `http://localhost:8081`.

***
### Testing
***

In order to run unit and functional tests after application setup, install the **pytest** package and simply run in the project folder: 

```shell
pip install pytest
```
```shell
DB_HOST=<your_host> pytest
```

***
## Docker Execution
***

To instantiate an application container and corresponding database with **docker-compose**, execute the following shell commands:

```shell
docker-compose up -d db
```
```shell
docker-compose build --no-cache
```
```shell
docker-compose run --rm flaskapp flask db upgrade
```
```shell
docker-compose up -d
```

The client should become available on `http://<host>:3000`.

***
## Automatic Deployment for Amazon EC2 Instances
***

### Create the necessary IAM Roles
***

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/26bulqgskw5bpu64r0kl.png)

One for the **EC2** instance:
  - _Trusted entity_: **AWS Service**
  - _Use Case_: **EC2**
  - _Policies_: **AmazonEC2RoleforAWSCodeDeploy**

  ![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/46kuzgo4qxpc639girdl.png)

  - Open configuration for the created _Role_ and edit _Trust Relationship_ as below:

  ![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/irtiqqgvv9uig7zxlist.png)

  ```json
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  }
  ```

Another one for the **CodeDeploy**
  - _Trusted entity_: **AWS Service**
  - _Use Case_: **EC2**
  - _Policies_: **AmazonEC2FullAccess**, **AWSCodeDeployFullAccess**, **AdministratorAccess**, **AWSCodeDeployRole**

  ![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y6l3k4yjo76yvbwu2ut1.png)

  - Open configurations for the created _Role_ and edit _Trust Relationship_ as below:
  
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "codedeploy.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
    ```

***
### Create the EC2 instance
***

For deployment testing, an **Amazon Linux 2 AMI (HVM), SSD Volume Type** machine with **64-bit (x86)** architecture and of type **t2.micro** was used

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tsbfckiuolr4y1oj5ilt.png)

In order to establish a connection between the **EC2** instance and the **CodeDeploy**, select the first _IAM Role_ created in the machine configuration.

In _Tags_ page, add a tag called **development**. The tag will require creating a _codeDeploy_ service.

In _Configure Security Group_, for practical purposes, configure _Type_ as **All traffic** and _Source_ as **Anywhere** (Not recommended for production).

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/c66iy10uzgmv6dygz5cl.png)

Initialize the instance and wait a few minutes.

***
### Installing CodeDeploy Agent in the EC2 Instance
***

When the created instance finishes launching, connect to it using the default _User name_.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wd9853dwfnc7hldoy7n9.png)

Use the following commands to install **codedeploy-agent**.

```shell
sudo yum update
```

```shell
sudo yum install -y ruby
```

```shell
sudo yum install wget
```

```shell
wget https://<bucket-name>.s3.<region-identifier>.amazonaws.com/latest/install
```
> Replace **bucket-name** and **region-identifier** by the [values corresponding to your region](https://docs.aws.amazon.com/codedeploy/latest/userguide/resource-kit.html#resource-kit-bucket-names)

```shell
chmod +x ./install
```

```shell
sudo ./install auto
```

```shell
sudo service codedeploy-agent start 
```

***
### Configure CodeDeploy Service
***

Create an _Application_ named **Git_Application** with _Compute platform_ **EC2/On-premises**

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hciskx6rrwq0r4m3whw6.png)

After that, create a _Deployment Group_ named **development_group**. For _Service role_, use _Role ARN_ from the **CodeDeploy_Role** created beforehand

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gqw1plmd8tpjscukpr7d.png)

Choose **In-place** for _Deployment type_. Select **Amazon Ec2 Instances** in _Environment configuration_ and add the _Tag key_ **development**

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/41sxab2cuhni6412y7f5.png)

Define **OneAtATime** for _Deployment settings_ and disable **Enable load balancing**

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3xivhirkebhcrl9ne7kb.png)

With the _Deployment Group_ ready, configure a new _Deployment_ with _Revision Type_ **My application is stored in GitHub**, activate **Connect to GitHub** after filling in your [GitHub token](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) and provide the _Repository name_ (**AnCaPepe/Flask-REST-Server-Weather** or your fork) and corresponding _Commit ID_ for the revision intended for usage.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3s5f3cv3auw4magmt33c.png)

Select **Overwrite the content** for _Content options_ and finish the _Deployment_ creation.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qya9yce6v5zxb09c21um.png)
  
Wait for the process to conclude. If a failure occurs, verify logs for the **EC2** instance at `/var/log/aws/codedeploy-agent/codedeploy-agent.log`.

***
### Configure GitHub Actions
***

In order to execute an automatic deployment after every change in your repository [fork](https://docs.github.com/en/github/getting-started-with-github/quickstart/fork-a-repo), create an [IAM user](https://docs.amazonaws.cn/en_us/IAM/latest/UserGuide/id_users_create.html#id_users_create_console) in **AWS** with _policy_ **AWSCodeDeployFullAccess** and generate [access key and secret access](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey) for it.

Define those as environment variables/secrets in your **GitHub** repo along with region information.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zkmvr6y8pi9aqpdjlj6b.png)