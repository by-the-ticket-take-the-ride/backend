find . -type f -name db.sqlite3 -exec rm -rf {} \;
find ./users -type d -name migrations -exec rm -rf {} \;
find ./api -type d -name migrations -exec rm -rf {} \;
find ./events -type d -name migrations -exec rm -rf {} \;
