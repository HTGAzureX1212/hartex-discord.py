import yaml

import discord


class ConfigurationValues:
    def __init__(self, configValue):
        self.configValue = configValue

# Roles


class OwnerRole(ConfigurationValues):
    with open('config.yaml', 'r') as IDAccessor:
        YAMLReader = yaml.safe_load(IDAccessor)

        ownerRoleID = YAMLReader['guild_configuration']['permission_levels']['roles']['owner']


class AdministratorRole(ConfigurationValues):
    with open('config.yaml', 'r') as IDAccessor:
        YAMLReader = yaml.safe_load(IDAccessor)

        adminRoleID = YAMLReader['guild_configuration']['permission_levels']['roles']['administrator']


class ModeratorRole(ConfigurationValues):
    with open('config.yaml', 'r') as IDAccessor:
        YAMLReader = yaml.safe_load(IDAccessor)

        moderRoleID = YAMLReader['guild_configuration']['permission_levels']['roles']['moderator']


# Enabled or disabled


class CommandsEnabledOrDisabled(ConfigurationValues):
    with open('config.yaml', 'r') as EnabledOrDisabled:
        YAMLReader = yaml.safe_load(EnabledOrDisabled)

        KickCommandEnabled = YAMLReader['plugins']['moderation']['commands']['kick']['general']['enabled']


class LoggingChannel(ConfigurationValues):
    with open('config.yaml', 'r') as LoggingChannels:
        YAMLReader = yaml.safe_load(LoggingChannels)

        MemberLoggingChannel = YAMLReader['plugins']['logging']['type']['member_log']['channel']

        MessageLoggingChannel = YAMLReader['plugins']['logging']['type']['message_log']['channel']
