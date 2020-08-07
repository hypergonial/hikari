# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2020 Nekokatt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Core interface for an object that serializes/deserializes API objects."""
from __future__ import annotations

__all__: typing.Final[typing.List[str]] = ["IEntityFactoryComponent"]

import abc
import typing

import attr

from hikari.api import component
from hikari.utilities import undefined

if typing.TYPE_CHECKING:

    from hikari.models import applications as application_models
    from hikari.models import audit_logs as audit_log_models
    from hikari.models import channels as channel_models
    from hikari.models import embeds as embed_models
    from hikari.models import emojis as emoji_models
    from hikari.models import gateway as gateway_models
    from hikari.models import guilds as guild_models
    from hikari.models import invites as invite_models
    from hikari.models import messages as message_models
    from hikari.models import presences as presence_models
    from hikari.models import users as user_models
    from hikari.models import voices as voice_models
    from hikari.models import webhooks as webhook_models
    from hikari.utilities import data_binding
    from hikari.utilities import files
    from hikari.utilities import snowflake


@attr.s(slots=True, weakref_slot=False)
class GatewayGuildDefinition:
    """A structure for handling entities within guild create and update events."""

    guild: guild_models.GatewayGuild = attr.ib()
    """Object of the guild the definition is for."""

    channels: typing.Optional[typing.Mapping[snowflake.Snowflake, channel_models.GuildChannel]] = attr.ib()
    """Mapping of channel IDs to the channels that belong to the guild.

    Will be `builtins.None` when returned by guild update gateway events rather
    than create.
    """

    members: typing.Optional[typing.Mapping[snowflake.Snowflake, guild_models.Member]] = attr.ib()
    """Mapping of user IDs to the members that belong to the guild.

    Will be `builtins.None` when returned by guild update gateway events rather
    than create.

    !!! note
        This may be a partial mapping of members in the guild.
    """

    presences: typing.Optional[typing.Mapping[snowflake.Snowflake, presence_models.MemberPresence]] = attr.ib()
    """Mapping of user IDs to the presences that are active in the guild.

    Will be `builtins.None` when returned by guild update gateway events rather
    than create.

    !!! note
        This may be a partial mapping of presences active in the guild.
    """

    roles: typing.Mapping[snowflake.Snowflake, guild_models.Role] = attr.ib()
    """Mapping of role IDs to the roles that belong to the guild."""

    emojis: typing.Mapping[snowflake.Snowflake, emoji_models.KnownCustomEmoji] = attr.ib()
    """Mapping of emoji IDs to the emojis that belong to the guild."""

    voice_states: typing.Optional[typing.Mapping[snowflake.Snowflake, voice_models.VoiceState]] = attr.ib()
    """Mapping of user IDs to the voice states that are active in the guild.

    !!! note
        This may be a partial mapping of voice states active in the guild.
    """


class IEntityFactoryComponent(component.IComponent, abc.ABC):
    """Interface for components that serialize and deserialize JSON payloads."""

    __slots__: typing.Sequence[str] = ()

    ######################
    # APPLICATION MODELS #
    ######################

    @abc.abstractmethod
    def deserialize_own_connection(self, payload: data_binding.JSONObject) -> application_models.OwnConnection:
        """Parse a raw payload from Discord into an own connection object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.applications.OwnConnection
            The deserialized "own connection" object.
        """

    @abc.abstractmethod
    def deserialize_own_guild(self, payload: data_binding.JSONObject) -> application_models.OwnGuild:
        """Parse a raw payload from Discord into an own guild object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.applications.OwnGuild
            The deserialized "own guild" object.
        """

    @abc.abstractmethod
    def deserialize_application(self, payload: data_binding.JSONObject) -> application_models.Application:
        """Parse a raw payload from Discord into an application object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.applications.Application
            The deserialized application object.
        """

    #####################
    # AUDIT LOGS MODELS #
    #####################

    @abc.abstractmethod
    def deserialize_audit_log(self, payload: data_binding.JSONObject) -> audit_log_models.AuditLog:
        """Parse a raw payload from Discord into an audit log object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.audit_logs.AuditLog
            The deserialized audit log object.
        """

    ##################
    # CHANNEL MODELS #
    ##################

    @abc.abstractmethod
    def deserialize_permission_overwrite(self, payload: data_binding.JSONObject) -> channel_models.PermissionOverwrite:
        """Parse a raw payload from Discord into a permission overwrite object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.channels.PermissionOverwrite
            The deserialized permission overwrite object.
        """

    @abc.abstractmethod
    def serialize_permission_overwrite(self, overwrite: channel_models.PermissionOverwrite) -> data_binding.JSONObject:
        """Serialize a permission overwrite object to a json serializable dict.

        Parameters
        ----------
        overwrite : hikari.models.channels.PermissionOverwrite
            The permission overwrite object to serialize.

        Returns
        -------
        hikari.utilities.data_binding.JSONObject
            The serialized representation of the permission overwrite.
        """

    @abc.abstractmethod
    def deserialize_partial_channel(self, payload: data_binding.JSONObject) -> channel_models.PartialChannel:
        """Parse a raw payload from Discord into a partial channel object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.channels.PartialChannel
            The deserialized "partial channel" object.
        """

    @abc.abstractmethod
    def deserialize_private_text_channel(self, payload: data_binding.JSONObject) -> channel_models.PrivateTextChannel:
        """Parse a raw payload from Discord into a DM channel object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.channels.PrivateTextChannel
            The deserialized DM channel object.
        """

    @abc.abstractmethod
    def deserialize_private_group_text_channel(
        self, payload: data_binding.JSONObject
    ) -> channel_models.GroupPrivateTextChannel:
        """Parse a raw payload from Discord into a group DM channel object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.channels.GroupPrivateTextChannel
            The deserialized group private text channel object.
        """

    @abc.abstractmethod
    def deserialize_guild_category(
        self,
        payload: data_binding.JSONObject,
        *,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
    ) -> channel_models.GuildCategory:
        """Parse a raw payload from Discord into a guild category object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.undefined.UndefinedOr[hikari.utilities.snowflake.Snowflake]
            The ID of the guild this channel belongs to. If passed then this
            will be prioritised over `"guild_id"` in the payload.

        !!! note
            `guild_id` currently only covers the gateway GUILD_CREATE event
            where `"guild_id"` is not included in the channel's payload.

        Returns
        -------
        hikari.models.channels.GuildCategory
            The deserialized guild category object.

        Raises
        ------
        KeyError
            If `guild_id` is left as `hikari.utilities.undefined.UNDEFINED` when
            `"guild_id"` is not present in the passed payload.
        """

    @abc.abstractmethod
    def deserialize_guild_text_channel(
        self,
        payload: data_binding.JSONObject,
        *,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
    ) -> channel_models.GuildTextChannel:
        """Parse a raw payload from Discord into a guild text channel object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.undefined.UndefinedOr[hikari.utilities.snowflake.Snowflake]
            The ID of the guild this channel belongs to. If passed then this
            will be prioritised over `"guild_id"` in the payload.

        !!! note
            `guild_id` currently only covers the gateway GUILD_CREATE event
            where `"guild_id"` is not included in the channel's payload.

        Returns
        -------
        hikari.models.channels.GuildTextChannel
            The deserialized guild text channel object.

        Raises
        ------
        KeyError
            If `guild_id` is left as `hikari.utilities.undefined.UNDEFINED` when
            `"guild_id"` is not present in the passed payload.
        """

    @abc.abstractmethod
    def deserialize_guild_news_channel(
        self,
        payload: data_binding.JSONObject,
        *,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
    ) -> channel_models.GuildNewsChannel:
        """Parse a raw payload from Discord into a guild news channel object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild this channel belongs to. If passed then this
            will be prioritised over `"guild_id"` in the payload.

        !!! note
            `guild_id` currently only covers the gateway GUILD_CREATE event
            where `"guild_id"` is not included in the channel's payload.

        Returns
        -------
        hikari.models.channels.GuildNewsChannel
            The deserialized guild news channel object.

        Raises
        ------
        KeyError
            If `guild_id` is left as `hikari.utilities.undefined.UNDEFINED` when
            `"guild_id"` is not present in the passed payload.
        """

    @abc.abstractmethod
    def deserialize_guild_store_channel(
        self,
        payload: data_binding.JSONObject,
        *,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
    ) -> channel_models.GuildStoreChannel:
        """Parse a raw payload from Discord into a guild store channel object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild this channel belongs to. If passed then this
            will be prioritised over `"guild_id"` in the payload.

        !!! note
            `guild_id` currently only covers the gateway GUILD_CREATE event
            where `"guild_id"` is not included in the channel's payload.

        Returns
        -------
        hikari.models.channels.GuildStoreChannel
            The deserialized guild store channel object.

        Raises
        ------
        KeyError
            If `guild_id` is left as `hikari.utilities.undefined.UNDEFINED` when
            `"guild_id"` is not present in the passed payload.
        """

    @abc.abstractmethod
    def deserialize_guild_voice_channel(
        self,
        payload: data_binding.JSONObject,
        *,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
    ) -> channel_models.GuildVoiceChannel:
        """Parse a raw payload from Discord into a guild voice channel object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild this channel belongs to. If passed then this
            will be prioritised over `"guild_id"` in the payload.

        !!! note
            `guild_id` currently only covers the gateway GUILD_CREATE event
            where `"guild_id"` is npt included in the channel's payload.

        Returns
        -------
        hikari.models.channels.GuildVoiceChannel
            The deserialized guild voice channel object.

        Raises
        ------
        KeyError
            If `guild_id` is left as `hikari.utilities.undefined.UNDEFINED` when
            `"guild_id"` is not present in the passed payload.
        """

    @abc.abstractmethod
    def deserialize_channel(
        self,
        payload: data_binding.JSONObject,
        *,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
    ) -> channel_models.PartialChannel:
        """Parse a raw payload from Discord into a channel object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.undefined.UndefinedOr[hikari.utilities.snowflake.Snowflake]
            The ID of the guild this channel belongs to. This will be ignored
            for DM and group DM channels and will be prioritised over
            `"guild_id"` in the payload when passed.

        !!! note
            `guild_id` currently only covers the gateway GUILD_CREATE event
            where `"guild_id"` is not included in the channel's payload.

        Returns
        -------
        hikari.models.channels.PartialChannel
            The deserialized partial channel-derived object.

        Raises
        ------
        KeyError
            If `guild_id` is left as `hikari.utilities.undefined.UNDEFINED` when
            `"guild_id"` is not present in the passed payload of a guild
            channel.
        """

    ################
    # EMBED MODELS #
    ################

    @abc.abstractmethod
    def deserialize_embed(self, payload: data_binding.JSONObject) -> embed_models.Embed:
        """Parse a raw payload from Discord into an embed object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.embeds.Embed
            The deserialized embed object.
        """

    @abc.abstractmethod
    def serialize_embed(
        self, embed: embed_models.Embed
    ) -> typing.Tuple[data_binding.JSONObject, typing.List[files.Resource[files.AsyncReader]]]:
        """Serialize an embed object to a json serializable dict.

        Parameters
        ----------
        embed : hikari.models.embeds.Embed
            The embed object to serialize.

        Returns
        -------
        typing.Tuple[hikari.utilities.data_binding.JSONObject, typing.List[hikari.utilities.files.Resource]]
            A tuple with two items in it. The first item will be the serialized
            embed representation. The second item will be a list of resources
            to upload with the embed.
        """

    ################
    # EMOJI MODELS #
    ################

    @abc.abstractmethod
    def deserialize_unicode_emoji(self, payload: data_binding.JSONObject) -> emoji_models.UnicodeEmoji:
        """Parse a raw payload from Discord into a unicode emoji object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.emojis.UnicodeEmoji
            The deserialized unicode emoji object.
        """

    @abc.abstractmethod
    def deserialize_custom_emoji(self, payload: data_binding.JSONObject) -> emoji_models.CustomEmoji:
        """Parse a raw payload from Discord into a custom emoji object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.emojis.CustomEmoji
            The deserialized custom emoji object.
        """

    @abc.abstractmethod
    def deserialize_known_custom_emoji(
        self, payload: data_binding.JSONObject, *, guild_id: snowflake.Snowflake
    ) -> emoji_models.KnownCustomEmoji:
        """Parse a raw payload from Discord into a known custom emoji object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild this emoji belongs to. This is used to ensure
            that the guild a known custom emoji belongs to is remembered by
            allowing for a context based artificial `guild_id` attribute.

        Returns
        -------
        hikari.models.emojis.KnownCustomEmoji
            The deserialized "known custom emoji" object.
        """

    @abc.abstractmethod
    def deserialize_emoji(
        self, payload: data_binding.JSONObject
    ) -> typing.Union[emoji_models.UnicodeEmoji, emoji_models.CustomEmoji]:
        """Parse a raw payload from Discord into an emoji object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.emojis.UnicodeEmoji or hikari.models.emojis.CustomEmoji
            The deserialized custom or unicode emoji object.
        """

    ##################
    # GATEWAY MODELS #
    ##################

    @abc.abstractmethod
    def deserialize_gateway_bot(self, payload: data_binding.JSONObject) -> gateway_models.GatewayBot:
        """Parse a raw payload from Discord into a gateway bot object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.gateway.GatewayBot
            The deserialized gateway bot object.
        """

    ################
    # GUILD MODELS #
    ################

    @abc.abstractmethod
    def deserialize_guild_widget(self, payload: data_binding.JSONObject) -> guild_models.GuildWidget:
        """Parse a raw payload from Discord into a guild widget object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.guilds.GuildWidget
            The deserialized guild widget object.
        """

    @abc.abstractmethod
    def deserialize_member(
        self,
        payload: data_binding.JSONObject,
        *,
        user: undefined.UndefinedOr[user_models.User] = undefined.UNDEFINED,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
    ) -> guild_models.Member:
        """Parse a raw payload from Discord into a member object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        user : hikari.utilities.undefined.UndefinedOr[hikari.models.users.User]
            The user to attach to this member, should only be passed in
            situations where "user" is not included in the payload.
        guild_id : hikari.utilities.undefined.UndefinedOr[hikari.utilities.snowflake.Snowflake]
            The ID of the guild this member belongs to. If this is specified
            then this will be prioritised over `"guild_id"` in the payload.

        !!! note
            `guild_id` covers cases such as the GUILD_CREATE gateway event and
            GET Guild Member where `"guild_id"` is not included in the returned
            payload.

        Returns
        -------
        hikari.models.guilds.Member
            The deserialized member object.

        Raises
        ------
        KeyError
            If `guild_id` is left as `hikari.utilities.undefined.UNDEFINED` when
            `"guild_id"` is not present in the passed payload.
        """

    @abc.abstractmethod
    def deserialize_role(
        self, payload: data_binding.JSONObject, *, guild_id: snowflake.Snowflake,
    ) -> guild_models.Role:
        """Parse a raw payload from Discord into a role object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.snowflake.Snowflake
            The ID of the guild this role belongs to. This is used to ensure
            that the guild a role belongs to is remembered by allowing for a
            context based artificial `guild_id` attribute.

        Returns
        -------
        hikari.models.guilds.Role
            The deserialized role object.
        """

    @abc.abstractmethod
    def deserialize_partial_integration(self, payload: data_binding.JSONObject) -> guild_models.PartialIntegration:
        """Parse a raw payload from Discord into a partial integration object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.guilds.PartialIntegration
            The deserialized partial integration object.
        """

    @abc.abstractmethod
    def deserialize_integration(self, payload: data_binding.JSONObject) -> guild_models.Integration:
        """Parse a raw payload from Discord into an integration object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.guilds.Integration
            The deserialized integration object.
        """

    @abc.abstractmethod
    def deserialize_guild_member_ban(self, payload: data_binding.JSONObject) -> guild_models.GuildMemberBan:
        """Parse a raw payload from Discord into a guild member ban object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.guilds.GuildMemberBan
            The deserialized guild member ban object.
        """

    @abc.abstractmethod
    def deserialize_guild_preview(self, payload: data_binding.JSONObject) -> guild_models.GuildPreview:
        """Parse a raw payload from Discord into a guild preview object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.guilds.GuildPreview
            The deserialized guild preview object.
        """

    @abc.abstractmethod
    def deserialize_rest_guild(self, payload: data_binding.JSONObject) -> guild_models.RESTGuild:
        """Parse a raw payload from Discord into a guild object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.guilds.RESTGuild
            The deserialized guild object.
        """

    @abc.abstractmethod
    def deserialize_gateway_guild(self, payload: data_binding.JSONObject) -> GatewayGuildDefinition:
        """Parse a raw payload from Discord into a guild object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        typing.Tuple[hikari.models.guilds.Guild ...]
            The deserialized guild object and the internal collections as
            maps of `hikari.utilities.snowflake.Snowflake` mapping to
            `hikari.models.channels.GuildChannel`,
            `hikari.models.guilds.Member`,
            `hikari.models.presences.MemberPresence`,
            `hikari.models.guilds.Role`, and
            `hikari.models.emojis.KnownCustomEmoji`. This is provided in
            several components to allow separate caching and linking
            between entities in various relational cache implementations
            internally.
        """

    #################
    # INVITE MODELS #
    #################

    @abc.abstractmethod
    def deserialize_vanity_url(self, payload: data_binding.JSONObject) -> invite_models.VanityURL:
        """Parse a raw payload from Discord into a vanity url object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.invites.VanityURL
            The deserialized vanity url object.
        """

    @abc.abstractmethod
    def deserialize_invite(self, payload: data_binding.JSONObject) -> invite_models.Invite:
        """Parse a raw payload from Discord into an invite object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.invites.Invite
            The deserialized invite object.
        """

    @abc.abstractmethod
    def deserialize_invite_with_metadata(self, payload: data_binding.JSONObject) -> invite_models.InviteWithMetadata:
        """Parse a raw payload from Discord into a invite with metadata object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.invites.InviteWithMetadata
            The deserialized invite with metadata object.
        """

    ##################
    # MESSAGE MODELS #
    ##################

    def deserialize_partial_message(self, payload: data_binding.JSONObject) -> message_models.PartialMessage:
        """Parse a raw payload from Discord into a partial message object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.messages.PartialMessage
            The deserialized partial message object.
        """

    @abc.abstractmethod
    def deserialize_message(self, payload: data_binding.JSONObject) -> message_models.Message:
        """Parse a raw payload from Discord into a message object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.messages.Message
            The deserialized message object.
        """

    ###################
    # PRESENCE MODELS #
    ###################

    @abc.abstractmethod
    def deserialize_member_presence(
        self,
        payload: data_binding.JSONObject,
        *,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
    ) -> presence_models.MemberPresence:
        """Parse a raw payload from Discord into a member presence object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.undefined.UndefinedOr[hikari.utilities.snowflake.Snowflake]
            The ID of the guild the presence belongs to. If this is specified
            then it is prioritised over `guild_id` in the payload.

        !!! note
            At the time of writing, the only place where `guild_id` will be
            mandatory is when parsing presences sent in a `GUILD_CREATE` event
            from Discord, since the `guild_id` attribute in the payload will
            have been omitted for redundancy.

        Returns
        -------
        hikari.models.presences.MemberPresence
            The deserialized member presence object.

        Raises
        ------
        KeyError
            If `guild_id` is not an attribute of the `payload` dict, and no
            guild ID was passed for the `guild_id` parameter.

            If this is raised, no guild ID info was provided anywhere.
        """

    ###############
    # USER MODELS #
    ###############

    @abc.abstractmethod
    def deserialize_user(self, payload: data_binding.JSONObject) -> user_models.User:
        """Parse a raw payload from Discord into a user object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.users.User
            The deserialized user object.
        """

    @abc.abstractmethod
    def deserialize_my_user(self, payload: data_binding.JSONObject) -> user_models.OwnUser:
        """Parse a raw payload from Discord into a user object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.users.OwnUser
            The deserialized user object.
        """

    ################
    # VOICE MODELS #
    ################

    @abc.abstractmethod
    def deserialize_voice_state(
        self,
        payload: data_binding.JSONObject,
        *,
        guild_id: undefined.UndefinedOr[snowflake.Snowflake] = undefined.UNDEFINED,
        member: undefined.UndefinedOr[guild_models.Member] = undefined.UNDEFINED,
    ) -> voice_models.VoiceState:
        """Parse a raw payload from Discord into a voice state object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.
        guild_id : hikari.utilities.undefined.UndefinedOr[hikari.utilities.snowflake.Snowflake]
            The ID of the guild this voice state belongs to. If this is specified
            then this will be prioritised over `"guild_id"` in the payload.
        member : hikari.utilities.undefined.UndefinedOr[hikari.models.guilds.Member]
            The object of the member this voice state belongs to. If this is
            specified then this will be prioritised over `"member"` in the
            payload.

        !!! note
            At the time of writing, `GUILD_CREATE` events are the only known
            place where neither `guild_id` nor `member` will be keys on the
            payload. In this case, you will need to provide the former
            parameters explicitly.

        Returns
        -------
        hikari.models.voices.VoiceState
            The deserialized voice state object.

        Raises
        ------
        KeyError
            If `guild_id` is left as `hikari.utilities.undefined.UNDEFINED` when
            `"guild_id"` is not present in the passed payload for the payload of
            the voice state.

            This will also be raised if no `member` data was passed in any
            acceptable place.
        """

    @abc.abstractmethod
    def deserialize_voice_region(self, payload: data_binding.JSONObject) -> voice_models.VoiceRegion:
        """Parse a raw payload from Discord into a voice region object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.voices.VoiceRegion
            The deserialized voice region object.
        """

    ##################
    # WEBHOOK MODELS #
    ##################

    @abc.abstractmethod
    def deserialize_webhook(self, payload: data_binding.JSONObject) -> webhook_models.Webhook:
        """Parse a raw payload from Discord into a webhook object.

        Parameters
        ----------
        payload : hikari.utilities.data_binding.JSONObject
            The JSON payload to deserialize.

        Returns
        -------
        hikari.models.webhooks.Webhook
            The deserialized webhook object.
        """
