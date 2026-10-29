FROM apache/hadoop:3.5.0

# Pre-create the directories so Docker initializes each new named volume with
# usable ownership.
USER root
RUN mkdir -p /hadoop/dfs/name /hadoop/dfs/data /hadoop/yarn/timeline \
    && chown -R hadoop:hadoop /hadoop
COPY --chown=hadoop:users config/ /opt/hadoop/etc/hadoop/

USER hadoop
ENTRYPOINT ["/usr/local/bin/dumb-init", "--", "/opt/starter.sh"]
