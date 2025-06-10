# SmogWatch 2. **Access the application:**
   - **Frontend:** http://localhost
   - **Backend API:** http://localhost/api (proxied through nginx)duction Deployment

This directory contains the production Docker configuration for the SmogWatch application.

## 🚀 Quick Start

1. **Build and start all services:**

   ```bash
   docker compose up --build -d
   ```

2. **Access the application:**
   - **Frontend:** <http://localhost>
   - **Backend API:** <http://localhost:5000>

## 📋 Available Commands

### Start Services

```bash
# Build and start in detached mode
docker compose up --build -d

# Start with logs visible
docker compose up --build
```

### Manage Services

```bash
# View service status
docker compose ps

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f frontend
docker compose logs -f backend

# Restart services
docker compose restart

# Stop services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

### Development Commands

```bash
# Rebuild specific service
docker compose build frontend
docker compose build backend

# Scale services (if needed)
docker compose up --scale backend=2 -d
```

## 🏗️ Architecture

- **Frontend:** Vue.js 3 application served by Nginx
- **Backend:** Flask API with Gunicorn WSGI server
- **Network:** Internal Docker bridge network for service communication

## 🔧 Configuration

### Environment Variables

The services use these production configurations:

- `FLASK_ENV=production`
- `PYTHONUNBUFFERED=1`

### Health Checks

Both services include health checks:

- **Backend:** HTTP check on port 5000
- **Frontend:** HTTP check on port 80

### Security Features

- Non-root users in containers
- Security headers in Nginx
- Proper file permissions
- Network isolation

## 📊 Monitoring

### Service Health

```bash
# Check health status
docker compose ps

# Check individual service health
docker inspect smogwatch-frontend --format='{{.State.Health.Status}}'
docker inspect smogwatch-backend --format='{{.State.Health.Status}}'
```

### Resource Usage

```bash
# View resource usage
docker stats

# View container info
docker compose top
```

## 🔧 Troubleshooting

### Common Issues

1. **Port conflicts:**

   ```bash
   # Check what's using port 80/5000
   sudo netstat -tulpn | grep :80
   sudo netstat -tulpn | grep :5000
   ```

2. **Service won't start:**

   ```bash
   # Check logs
   docker compose logs frontend
   docker compose logs backend
   
   # Check health
   docker compose ps
   ```

3. **API connection issues:**
   - Verify backend is healthy via nginx proxy: `curl http://localhost/api/`
   - Check Nginx proxy configuration in `frontend/nginx.conf`
   - Backend is not directly accessible from outside the container network

### Debug Mode

```bash
# Run services with debug output
docker compose up --build

# Run specific service interactively
docker compose run --rm backend bash
docker compose run --rm frontend sh
```

## 🚀 Production Considerations

### Performance

- Nginx serves static files efficiently
- Gunicorn provides multiple worker processes
- Gzip compression enabled
- Static asset caching configured

### Security

- Non-root users in all containers
- Security headers configured
- Network isolation between services
- Health checks for monitoring

### Scaling

To scale for higher load:

```bash
# Scale backend workers
docker compose up --scale backend=3 -d

# Add load balancer (nginx upstream) if needed
```
