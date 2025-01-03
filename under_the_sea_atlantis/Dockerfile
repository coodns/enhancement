FROM ghcr.io/runatlantis/atlantis:sha256-520b99a7f1560718571c7432e32a634ebd04d2d31582e3ca46b161b55eeca835

RUN atlantis server \
--atlantis-url="$URL" \
--gitlab-user="$USERNAME" \
--gitlab-token="$TOKEN" \
--gitlab-webhook-secret="$SECRET" \
--repo-allowlist="$REPO_ALLOWLIST"