#adas
MAKEFLAGS += --silent
help:
	@printf '\nmake [options]\n'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%10s\033[0m %s\n", $$1, $$2}'

pull: ## get updates from cloud
	git pull -q

put: ## put local udpates to cloud
	- git add *
	- git commit -am saving --quiet
	- git push --quiet -u --no-progress
	- git status --short

