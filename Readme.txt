Here are the list of all the poilcy you have to attache to your ec2 


1:- AmazonSSMManagedInstanceCore = to give access to your instance to connect to ssm
2:- AmazonSSMPatchAssociation = this is also do the same
3:- CloudWatchAgentServerPolicy = this is allow your cloud watch to keep track of your ec2 instance
4:- than you have to create your 3 custom policy which are resposnible to get ssm stored parameter
 And allow it to get and put in s3 bucket and to get read from ECR

                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "AllowgetParameterByPath",
                                "Effect": "Allow",
                                "Action": [
                                    "ssm:GetParametersByPath",
                                    "ssm:GetParameter",
                                    "ssm:GetParameters"
                                ],
                                "Resource": "*"
                            }
                        ]
                    }


-----------------------------------------------------------------------------------------------------------------
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": [
                                    "s3:GetObject"
                                ],
                                "Resource": "arn:aws:s3:::416394563192-devops-script/*"
                            },
                            {
                                "Effect": "Allow",
                                "Action": [
                                    "s3:ListBucket"
                                ],
                                "Resource": "arn:aws:s3:::416394563192-devops-script"
                            }
                        ]
                    }
-------------------------------------------------------------------------------------------------------------

                        {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Action": [
                                        "ecr:GetAuthorizationToken",
                                        "ecr:BatchCheckLayerAvailability",
                                        "ecr:ListImages",
                                        "ecr:DescribeImages",
                                        "ecr:BatchGetImage",
                                    ],
                                    "Resource": "*"
                                }
                            ]
                        }



Now we have to do create a github Action role so it can access our Resource in aws but only limited

1:- this is to give access to s3 ducket so it can put and get files 
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "S3Script",
			"Effect": "Allow",
			"Action": [
				"s3:CreateBucket",
				"s3:PutObject",
				"s3:GetObject"
			],
			"Resource": [
				"*"
			]
		}
	]
}

2:- to invoke commnads 

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "SSMGIT",
			"Effect": "Allow",
			"Action": [
				"ssm:SendCommand",
				"ssm:GetCommandInvocation",
				"ssm:ListCommandInvocations"
			],
			"Resource": "*"
		}
	]
}

3:- this is for i can get and put images on ECR 

{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"ecr:GetAuthorizationToken",
				"ecr:BatchGetImage",
				"ecr:BatchCheckLayerAvailability",
				"ecr:CompleteLayerUpload",
				"ecr:GetDownloadUrlForLayer",
				"ecr:InitiateLayerUpload",
				"ecr:PutImage",
				"ecr:UploadLayerPart"
			],
			"Resource": "*"
		}
	]
}




3:- Must run this command in your both instances 


#!/bin/bash
set -e

cat > /home/ubuntu/deploy.sh << 'EOF'
#!/bin/bash
set -e

# Configurations
BUCKET_NAME="416394563192-devops-script"
COMPOSE_FILE="docker-compose.yml"
TARGET_DIR="/home/ubuntu"
REGISTRY="416394563192.dkr.ecr.us-east-1.amazonaws.com"

echo "1. Fetching latest docker-compose.yml from S3..."
aws s3 cp s3://$BUCKET_NAME/$COMPOSE_FILE $TARGET_DIR/$COMPOSE_FILE

echo "2. Logging into AWS ECR..."
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $REGISTRY

echo "3. Pulling latest images..."
docker compose -f $TARGET_DIR/$COMPOSE_FILE pull

echo "4. Restarting application stack..."
docker compose -f $TARGET_DIR/$COMPOSE_FILE up -d

echo "5. Cleaning up stale images..."
docker system prune -f

echo "✅ Deployment complete!"
EOF

chmod +x /home/ubuntu/deploy.sh

chown ubuntu:ubuntu /home/ubuntu/deploy.sh

echo "deploy.sh created successfully."