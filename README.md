# Digital Library

A Flask-based digital library application with admin panel, interactive book display, and click analytics.

## Features

- Admin panel with secure password access
- Interactive book display with clickable covers
- Download and share functionality
- Click analytics tracking
- Mobile-responsive book grid layout
- Support for both direct PDF uploads and external book URLs

## Deployment on Railway

### Step 1: Create a Railway Account

1. Go to [Railway.app](https://railway.app/) and sign up for an account
2. Install the Railway CLI: `npm i -g @railway/cli`
3. Login: `railway login`

### Step 2: Create a New Project

1. Create a new project in the Railway dashboard
2. Add a PostgreSQL database to your project from the Railway dashboard

### Step 3: Configure Environment Variables

Set the following environment variables in your Railway project settings:

- `SECRET_KEY`: A secure random string for session encryption
- `DATABASE_URL`: This will be automatically set by Railway when you add PostgreSQL
- `ADMIN_USERNAME`: Your desired admin username (e.g., railway_admin)
- `ADMIN_EMAIL`: Your admin email address
- `ADMIN_PASSWORD`: A secure password for your admin account
- `RAILWAY_ENVIRONMENT`: Set to "production"

### Step 4: Deploy the Application

1. Link your local repository to your Railway project:
   ```
   railway link
   ```

2. Deploy the application:
   ```
   railway up
   ```

3. After deployment, run the setup script to configure the database and admin user:
   ```
   railway run python railway_setup.py
   ```

### Step 5: Access Your Application

1. Your application will be deployed at a URL provided by Railway
2. Log in with the admin credentials you set in the environment variables

## Local Development

1. Clone the repository
2. Install dependencies
3. Set environment variables
4. Run the application with `python main.py`

## License

MIT