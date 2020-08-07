import asyncio
import emoji
import discord
from functions import random_choose
from interpreter.conditions import MessageConditions

class Interpreter:
    async def message_and_reply(self,
        message: discord.Message,
        conditions = None,
        expected_message = None,
        reply = None,
        reaction = None):

        self.expected_message = expected_message

        message_condition = MessageConditions(
            message,
            expected_message = expected_message
        )

        all_condition_is_true = False
        if conditions:
            if type(conditions) == list:
                conditions_to_confirm = []
                for each_conditions in conditions:
                    conditions_to_confirm.append(message_condition.string_conditions[each_conditions])
            else:
                conditions_to_confirm = [message_condition.string_conditions[conditions]]
            
            all_condition_is_true = conditions_to_confirm.count(True) == len(conditions_to_confirm)

        if all_condition_is_true or conditions == None:
            await Interpreter.send_reply(self, reply, message)
            await Interpreter.send_reaction(self, reaction, message)

    async def send_reaction(self, reaction, message:discord.Message):
        if reaction:
            if type(reaction) == list:
                for each_reaction in reaction:
                    each_reaction = random_choose(each_reaction) if type(each_reaction) == list else each_reaction
                    each_reaction = emoji.emojize(each_reaction, use_aliases = True)
                    try:
                        await message.add_reaction(each_reaction)
                    except discord.HTTPException:
                        print(each_reaction)
            else:
                try:
                    reaction = emoji.emojize(reaction, use_aliases = True)
                    await message.add_reaction(reaction)
                except discord.HTTPException:
                    print(reaction)

    async def send_reply(self, reply, message:discord.Message):
        if reply:
            if type(reply) == list:
                for each_reply in reply:
                    each_reply = random_choose(each_reply) if type(each_reply) == list else each_reply
                    await message.channel.send(each_reply)
            else:
                await message.channel.send(each_reply)