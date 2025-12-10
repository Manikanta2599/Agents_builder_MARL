#!/bin/bash
echo "🚀 Pushing Anti-Gravity System to GitHub..."
echo "Target: https://github.com/Manikanta2599/Agents_builder_MARL.git"
echo "---------------------------------------------------"

# Ensure origin is correct
git remote set-url origin https://github.com/Manikanta2599/Agents_builder_MARL.git

# Attempt push
git push -u origin main

echo "---------------------------------------------------"
if [ $? -eq 0 ]; then
  echo "✅ Push Success! View at: https://github.com/Manikanta2599/Agents_builder_MARL"
else
  echo "❌ Push Failed."
  echo "Please ensure you are logged in using:"
  echo "  gh auth login"
  echo "OR use a Personal Access Token as your password."
fi