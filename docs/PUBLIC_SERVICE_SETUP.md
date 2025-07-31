# Public Service Setup Guide

This guide explains how to deploy the playlist importer as a public web service where users can access it via browser without any technical setup.

## 🏗️ **Architecture Overview**

### **Multi-User Features**
- ✅ **User Session Management** - Each user gets a unique session
- ✅ **Database Storage** - OAuth tokens stored securely per user
- ✅ **No Local Files** - Everything runs in the cloud
- ✅ **Public OAuth** - Users authenticate with their own accounts

### **User Experience**
1. **Visit website** - No setup required
2. **Click "Connect Spotify"** - Standard OAuth login
3. **Click "Connect YouTube"** - Standard OAuth login
4. **Select playlist** - Browse their Spotify playlists
5. **Import to YouTube** - Creates playlist in their YouTube account

## 🚀 **Deployment Options**

### **Option 1: Railway (Recommended)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### **Option 2: Heroku**
```bash
# Install Heroku CLI
# Create Procfile
echo "web: uvicorn multi_user_main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### **Option 3: DigitalOcean App Platform**
- Upload code to GitHub
- Connect to DigitalOcean App Platform
- Set environment variables
- Deploy

## ⚙️ **Environment Setup**

### **1. Environment Variables**
Set these in your deployment platform:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=https://your-domain.com/callback
DATABASE_URL=postgresql://user:pass@host:port/db
```

### **2. OAuth Configuration**

#### **Spotify Developer Dashboard**
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Update your app's Redirect URIs:
   - Add: `https://your-domain.com/callback`
   - Remove: `http://localhost:3000/callback`

#### **Google Cloud Console**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Update OAuth 2.0 credentials:
   - Change from "Desktop application" to "Web application"
   - Add Authorized redirect URIs:
     - `https://your-domain.com/youtube/callback`
   - Add Authorized JavaScript origins:
     - `https://your-domain.com`

### **3. Database Setup**
The service uses PostgreSQL for production:

```sql
-- Database will be created automatically
-- Tables will be created by SQLAlchemy
```

## 📁 **Files for Public Service**

### **Core Files**
- `multi_user_main.py` - Multi-user FastAPI application
- `models.py` - Database models for user management
- `multi_user_youtube_api.py` - Multi-user YouTube API client
- `requirements_public.txt` - Dependencies for public service

### **Configuration Files**
- `Procfile` - For Heroku deployment
- `runtime.txt` - Python version specification
- `.env` - Environment variables (set in deployment platform)

## 🔧 **Deployment Steps**

### **Step 1: Prepare Code**
```bash
# Copy multi-user files
cp multi_user_main.py main.py
cp requirements_public.txt requirements.txt

# Create Procfile for Heroku
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

### **Step 2: Set Environment Variables**
In your deployment platform, set:
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI`
- `DATABASE_URL` (if using external database)

### **Step 3: Deploy**
```bash
# For Railway
railway up

# For Heroku
git add .
git commit -m "Deploy multi-user version"
git push heroku main
```

### **Step 4: Update OAuth Settings**
1. Update Spotify redirect URIs
2. Update Google Cloud OAuth settings
3. Test authentication flows

## 🔒 **Security Considerations**

### **Data Protection**
- ✅ **User tokens encrypted** in database
- ✅ **No sensitive data logged**
- ✅ **CORS configured** for your domain
- ✅ **HTTPS required** for OAuth

### **Privacy**
- ✅ **User data isolated** per session
- ✅ **No cross-user data sharing**
- ✅ **Tokens expire** automatically
- ✅ **GDPR compliant** token storage

## 📊 **Monitoring & Analytics**

### **Health Checks**
```bash
# Check service health
curl https://your-domain.com/health

# Check database status
curl https://your-domain.com/health
```

### **User Analytics**
- Track successful imports
- Monitor authentication success rates
- Log error patterns

## 🚨 **Troubleshooting**

### **Common Issues**

1. **"OAuth redirect URI mismatch"**
   - Update redirect URIs in Spotify/Google Cloud Console
   - Ensure HTTPS URLs for production

2. **"Database connection failed"**
   - Check DATABASE_URL environment variable
   - Verify database is accessible

3. **"YouTube API quota exceeded"**
   - Monitor API usage in Google Cloud Console
   - Consider upgrading quota limits

4. **"Spotify authentication failed"**
   - Verify CLIENT_ID and CLIENT_SECRET
   - Check redirect URI configuration

### **Debug Mode**
```bash
# Run locally for testing
python multi_user_main.py

# Check logs
railway logs
heroku logs --tail
```

## 🎯 **User Experience**

### **For End Users**
1. **Visit website** - No technical setup
2. **Authenticate** - Standard OAuth flows
3. **Import playlists** - One-click operation
4. **Access playlists** - Direct YouTube links

### **Benefits**
- ✅ **No technical knowledge required**
- ✅ **Works on any device**
- ✅ **Secure authentication**
- ✅ **Fast and reliable**

## 📈 **Scaling Considerations**

### **Performance**
- **Database indexing** for user queries
- **Token caching** for faster authentication
- **API rate limiting** to prevent abuse

### **Cost Optimization**
- **Database connection pooling**
- **Efficient token storage**
- **API quota management**

## 🎉 **Ready for Public Use**

Once deployed, users can:
1. **Visit your website**
2. **Connect their Spotify account**
3. **Connect their YouTube account**
4. **Import playlists seamlessly**

The service handles all the complexity behind the scenes! 🚀 