tr -sc "[:alpha:]" "\n" < $1 | tr A-Z a-z | sort | uniq -c | sort -n -r
