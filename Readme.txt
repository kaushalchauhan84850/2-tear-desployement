Must run this command in your both instances 


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