BASE_URL="http://98.80.38.242"  # example: "http://myazuremachine.eastus.cloudapp.azure.com"

# webarena environment variables (change ports as needed)
export WA_SHOPPING="$BASE_URL:7770/"
export WA_SHOPPING_ADMIN="$BASE_URL:7770/admin"
export WA_REDDIT="$BASE_URL:9999"
export WA_GITLAB="$BASE_URL:8023"
export WA_WIKIPEDIA="$BASE_URL:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"
export WA_MAP="$BASE_URL:3000"
export WA_HOMEPAGE="$BASE_URL:4399"

# if your webarena instance offers the FULL_RESET feature (optional)
export WA_FULL_RESET="$BASE_URL:7565"

# otherwise, be sure to NOT set WA_FULL_RESET, or set it to an empty string
export WA_FULL_RESET=""

# export DATASET=visualwebarena

# export CLASSIFIEDS="http://98.80.38.242:9980"
# export CLASSIFIEDS_RESET_TOKEN="4b61655535e7ed388f0d40a93600254c"  # Default reset token for classifieds site, change if you edited its docker-compose.yml
# export SHOPPING="http://98.80.38.242:7770"
# export REDDIT="http://98.80.38.242:9999"
# # export WIKIPEDIA="http://98.80.38.242:8888"
# export WIKIPEDIA="http://98.80.38.242:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"
# export HOMEPAGE="http://98.80.38.242:4399"

# export SHOPPING_ADMIN="http://98.80.38.242:7780/admin"
# export GITLAB="http://98.80.38.242:8023"
# export MAP="http://98.80.38.242:3000"

# export STORE="http://98.80.38.242:1201/"