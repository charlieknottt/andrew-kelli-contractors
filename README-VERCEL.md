# Deploying Andrew and Kelli Contractors App to Vercel

## Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Create a Vercel account at https://vercel.com
3. Ensure you have Git initialized in your project

## Deployment Steps

1. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   ```

2. **Deploy to Vercel:**
   ```bash
   vercel
   ```
   - Follow the prompts
   - Choose "Y" to link to existing project or create new
   - Set project name (e.g., "andrew-kelli-contractors")
   - Confirm the settings

3. **Configure Environment (if needed):**
   - The app should work out of the box
   - Files will be stored temporarily in `/tmp` on Vercel

## Important Notes

- **File Storage**: Vercel is serverless, so uploaded files are temporary
- **Limitations**: Each function has a 10-second timeout and 50MB memory limit
- **OpenCV**: Using `opencv-python-headless` for better serverless compatibility
- **Reports**: PDF reports are generated in memory and served directly

## Custom Domain (Optional)
- Go to your Vercel dashboard
- Add your custom domain in project settings
- Update DNS records as instructed

## Files Added for Vercel:
- `vercel.json` - Vercel configuration
- `.vercelignore` - Files to ignore during deployment
- `runtime.txt` - Python version specification
- Updated `requirements.txt` with `opencv-python-headless`

## Accessing Your App
After deployment, Vercel will provide a URL like:
`https://your-project-name.vercel.app`