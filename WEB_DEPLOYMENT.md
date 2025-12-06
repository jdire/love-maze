# Love Maze - Web Deployment Guide

## Quick Deploy (Recommended)

The game has been built for web using Pygbag. The web-ready files are in the `build/web/` folder.

### Testing Locally

The development server is running at: **http://localhost:8000**

Open this URL in your browser to play the game!

### Deploy to Production

Upload the **entire `build/web/` folder** to any static hosting service:

#### Option 1: GitHub Pages (Free & Easy)

1. Create a new repository on GitHub (or use existing)
2. Go to Settings → Pages
3. Upload the contents of `build/web/` to your repository
4. Your game will be live at: `https://yourusername.github.io/repository-name/`

#### Option 2: Netlify (Drag & Drop)

1. Go to https://netlify.com
2. Drag the `build/web/` folder onto Netlify
3. Get instant URL like: `https://your-game.netlify.app`

#### Option 3: Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `cd build/web && vercel`
3. Get instant deployment URL

#### Option 4: GitHub Pages via Terminal

```bash
cd build/web
git init
git add .
git commit -m "Deploy Love Maze"
git branch -M main
git remote add origin https://github.com/yourusername/love-maze.git
git push -u origin main
```

Then enable GitHub Pages in repository settings.

## Rebuilding for Web

If you make changes to the game, rebuild with:

```bash
.venv/bin/python -m pygbag --build .
```

## Mobile Controls

The web version supports:
- **Touch/Tap**: Click/tap where you want the ring to move
- **Swipe**: Quick directional movement
- **Keyboard**: Arrow keys or WASD (desktop)

## Notes

- The game runs in WebAssembly via Pygame Web
- Audio is simplified for web compatibility
- All touch controls work on mobile browsers
- No installation needed - runs in any modern browser
