echo "Cleaning up..."
rm -rf page
mkdir page
git worktree prune
rm -rf .git/worktrees/page/

echo "Checking out gh-pages branch..."
git worktree add -B gh-pages page origin/gh-pages

echo "Removing contents..."
rm -rf page/*

echo "Building static website..."
python main.py
cp -r css page/

echo "Done!"
