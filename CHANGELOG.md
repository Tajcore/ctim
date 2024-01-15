# CHANGELOG



## v0.1.1 (2024-01-15)

### Fix

* fix(platform): corrected the command to run the tests in the CI ([`93ddc1d`](https://github.com/thompsonson/ctim/commit/93ddc1d59e9ef5a9862b527f639cb7b6a6f49d60))


## v0.1.0 (2024-01-15)

### Chore

* chore: automating tests on this branch ([`3697044`](https://github.com/thompsonson/ctim/commit/3697044ffe9e0c13ea8d0ac2c5ed57227be4be43))

* chore: tests for Ransomware code prior to moving and adding telegram code ([`0a84e2c`](https://github.com/thompsonson/ctim/commit/0a84e2c8319d7503bc99f601cd9c2ee46b82515e))

* chore: adding digital ocean integration test environment ([`56d4a89`](https://github.com/thompsonson/ctim/commit/56d4a89a95e17bd1d33f856ccf7ffc2346e77f20))

* chore: ensure indempotence on group and post updates ([`4f57ae4`](https://github.com/thompsonson/ctim/commit/4f57ae4e8ea7b54a69426bf9ce2b02e34a332508))

* chore: painted it black and more chores ([`f72c3be`](https://github.com/thompsonson/ctim/commit/f72c3be5f70dfca30f2977b2fc04d9e208150eec))

### Feature

* feat(platform): cleaning up imports and adding a step to clear the cache in the CI pipeline ([`ad613fc`](https://github.com/thompsonson/ctim/commit/ad613fc185e32f6797f895443a6ad3763dce84df))

* feat(platform): automated semantic release generation on a pull request ([`fc52c4a`](https://github.com/thompsonson/ctim/commit/fc52c4a1a7b38f27459650205079ed87bd4c9773))

* feat(telegram): downloads telegram channel posts for a given channel ([`eb8827c`](https://github.com/thompsonson/ctim/commit/eb8827c5239ec2b68639c521d1af6c012274ad8d))

* feat(platform): adding celery to the platform (to manage the scrapping tasks) ([`b003d10`](https://github.com/thompsonson/ctim/commit/b003d10dd5b65a1786c17d357d8689eab88ae051))

* feat(telegram): model update for ChannelPost and management command to doanload all Channel Posts for a given channel ([`7f79225`](https://github.com/thompsonson/ctim/commit/7f79225c4cad866f9c67785d186cb6674fc26a31))

* feat(telegram): models for storing Telegram messages and tests ([`b689b3e`](https://github.com/thompsonson/ctim/commit/b689b3e55509aa8de7d4e5f7ec42387454ac5bbf))

* feat(test_environment): Code for Digital Ocean based Integration Environment ([`a22b48a`](https://github.com/thompsonson/ctim/commit/a22b48acfb1a1c4a0987449aa5c6c0ffdeb6bbc3))

* feat: imports the ransomware posts and makes them available, via a RESTful API to the OpenAI GPT ([`30c5261`](https://github.com/thompsonson/ctim/commit/30c526106de764d86a08c6f6cd3af2b9c1afb99b))

* feat: imports the ransomware groups and makes them available, via a RESTful API to the OpenAI GPT ([`0db0662`](https://github.com/thompsonson/ctim/commit/0db0662cda3b3c1bd3f3e83602c4de64431d417d))

* feat: oauth server works with OpenAI GPT and the oauth client works with Github (needs cleaning, but it WORKS :) ([`1b2699b`](https://github.com/thompsonson/ctim/commit/1b2699b93cd6a8f31102020e5d0202dcb216e7a7))

### Unknown

* Merge pull request #12 from thompsonson/telegram

Telegram ([`7948c6f`](https://github.com/thompsonson/ctim/commit/7948c6f773a3fb9ac97bb871007f23ca2cda3f2e))

* Merge branch &#39;main&#39; into telegram ([`8272fc8`](https://github.com/thompsonson/ctim/commit/8272fc8db60411e6053fe862366d2a85abff06fb))

* ui: tidied the sign up and sign in pages. ([`78dcaa6`](https://github.com/thompsonson/ctim/commit/78dcaa6fb17066570d0aa9d512aca3518d39da75))

* Fix: pre-commit issues ([`5538a61`](https://github.com/thompsonson/ctim/commit/5538a61d62900585b6b64bfd654c0c5df78af54e))
