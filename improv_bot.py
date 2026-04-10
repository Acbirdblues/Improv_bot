import discord
from discord.ext import commands
import random
import json
from datetime import datetime

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ============= SCENE DATABASES =============
SCENES_2 = [
    {
        "text": "Sarah sits at her kitchen table with cold coffee. She's 52, wearing glasses on a chain. Her daughter Emma arrives after 8 months away. They haven't been in the same room in eight months. Sarah stands too quickly, knocks over a plant. Emma picks it up. Sarah says \"I can get that\" but doesn't move. Emma notices the house is impossibly clean—prepared for inspection. There's tension between them, familiar yet new. Emma puts the plant back. Sarah asks \"Coffee?\" Emma says \"It's almost midnight.\" Sarah says \"I know.\" They stand there, distance feeling like three years and three inches.",
        "themes": "Sarah: LONGING (hopeful→resigned). Emma: GUILT (defensive→cracking)."
    },
    {
        "text": "Robert, 65 and newly retired, reorganizes bookshelves for the third time. His son David arrives unannounced. David is 35, successful in career but destroyed in personal life—marriage two is falling apart. He comes home when he needs advice or money or escape. Robert doesn't look up. \"You're going to figure it out,\" he says. David throws his bag down. \"I already figured it out twice, Dad.\" Robert turns. \"Your mother and I had problems too. But we didn't run every time.\" David feels something calcify in his chest. \"Yeah, and look how great that worked.\" Robert turns back to books. The silence is decades of unsaid things.",
        "themes": "Robert: DISAPPOINTMENT (resigned, judging). David: DEFENSIVENESS (ashamed, running)."
    },
    {
        "text": "Monica and Jessica meet Tuesday for coffee like they do every week for 7 years. Jessica reveals her daughter got into Yale—full scholarship. Monica has been trying to get pregnant for 5 years. Nobody knows. She hasn't told anyone. Monica says \"That's amazing.\" But her voice breaks. Jessica reaches to hold her hand. Monica pulls away. \"I'm so happy for you,\" Monica says, and means it, and hates herself for how much it costs to say that and mean it simultaneously.",
        "themes": "Jessica: JOY COMPLICATED BY GUILT (sensing hurt). Monica: ENVY (aching, resentful, isolated)."
    }
]

SCENES_3 = [
    {
        "text": "Marcus and Alex sit in a dark conference room after 5pm. Marcus has been at the firm 15 years—meticulous, reliable, stays late without complaining. Alex is 32, sharp, ambitious—promoted twice in three years. The promotion Marcus wanted goes to Alex. Marcus found out accidentally. Alex wanted to tell him first. Now Alex tries to navigate this minefield. Marcus arranges papers—not because he needs to, but because his hands need something to do. Alex says \"We need to talk.\" Marcus says \"I'm busy.\" Alex sits anyway. Marcus keeps arranging. Alex says \"I didn't ask for this.\" Marcus finally looks at him. \"Yeah you did. Last year. And the year before. You asked for it. You just didn't think it would cost anything.\" Alex says \"That's not fair.\" Marcus looks back down. \"Isn't it?\"",
        "themes": "Marcus: RESENTMENT (guarded, justified rage). Alex: GUILT (seeking forgiveness, defensive)."
    },
    {
        "text": "Carol stands in the lobby of the hotel where her daughter's wedding will happen in one hour. They haven't spoken in 3 months—she's marrying someone from a different religion. Carol told her: \"Not welcome in this family.\" Now she's here in the lobby in her dress, tears threatening. Her ex-husband appears holding tissues. \"I thought you wouldn't come,\" he says gently. Carol looks at decorations being set up. \"I almost didn't. I wanted her to know what she's losing.\" He sits heavily. \"Carol, she knows exactly what she's losing. She's chosen it anyway. Maybe that means she's not actually losing anything that matters.\"",
        "themes": "Carol: RIGHTEOUS ANGER (rigid, unable to bend). Ex-husband: SORROW (accepting loss, seeing clearly)."
    },
    {
        "text": "Tom and Steve stand in the garage of their childhood home. Their mother died 3 weeks ago. They're supposed to divide her belongings. Tom lives in New York running a Fortune 500 company. Steve stayed home running the family hardware store. Tom looks at boxes. \"We should hire an estate company. I have a meeting Monday.\" Steve stares at him. \"This is Mom's life, Tom.\" Tom says \"I know, but—\" Steve says quietly \"She called me every day last year asking if you were coming. Every single day. And you never did.\" Tom feels defensive rising. \"I called her.\" Steve says \"Once a month. For ten minutes. While you were in your car.\" Tom says \"I built a company, Steve.\" Steve says \"And someone had to be here.\"",
        "themes": "Tom: GUILT MASKED AS AMBITION (defensive, dismissive). Steve: RESENTMENT MASKED AS LOYALTY (exhausted from staying)."
    }
]

SCENES_4 = [
    {
        "text": "James sits in a therapist's office for the first time. The room is small with soft lighting and a beige couch that's seen a thousand conversations. There's a framed abstract print on the wall—something meant to be calming but unsettling. Dr. Chen sits in a chair with a notepad. She's 60, calm, professional—heard everything, judges nothing. James postponed this 3 years. His wife gave ultimatum last Tuesday: \"Therapy or I'm done.\" James looks at the floor. His shirt has a coffee stain from this morning. Dr. Chen opens her notepad and clicks her pen. \"So James, what brought you in?\" James says \"My wife.\" Dr. Chen writes. \"Tell me about her.\" James looks up and there's something breaking. \"That's it, Dr. Chen. I can't. That's why I'm here. I can't talk about her. I can't talk about any of it. I'm drowning.\"",
        "themes": "James: FEAR OF EXPOSURE (shame, isolation, trapped). Dr. Chen: PROFESSIONAL COMPASSION (patient, unbothered)."
    },
    {
        "text": "Anna sits across from Michael in his office at end of day. Building is empty. Michael is 50, founder. Anna is 28, most talented but invisible—never advocated for herself. Michael watched her diminish for 2 years. Today he called her to offer promotion to lead designer. Anna's hands shake. \"I don't know if I'm ready.\" Michael leans back. \"Anna, you've been ready a year. You're the most talented I've worked with.\" Anna says \"But what if I fail?\" Michael says \"Then you fail. But I think what you're really afraid of is succeeding. Because then you'd have to stop hiding. Because people would see you. And that terrifies you more than failure ever could.\"",
        "themes": "Anna: FEAR OF VISIBILITY (self-doubt, imposter syndrome). Michael: FRUSTRATED COMPASSION (seeing potential, can't force belief)."
    },
    {
        "text": "Rachel and her mother Helen sit in a car in a parking lot. Rachel just got news she'll never have biological children. She's 37. Helen is 65, already grandmother to Rachel's two adopted kids. She knows what's coming—grief, rage, unfairness. Rachel stares straight ahead. Helen doesn't look at her. \"I wanted to tell you when you were younger that life doesn't go according to plan. But I feared you'd stop trying.\" Rachel says \"Well, I stopped trying.\" Helen says \"Your kids are upstairs with the sitter. Waiting for you. They don't care how you got them. They care you're theirs.\" Rachel says \"That doesn't make this hurt less.\" Helen says \"No. But it might make it matter less.\"",
        "themes": "Rachel: DEVASTATION & DENIAL (grieving what she'll never have). Helen: HARD-EARNED WISDOM (acceptance, offering perspective Rachel isn't ready for)."
    }
]

# ============= FEEDBACK RESPONSES =============
FEEDBACK_LEVELS = {
    1: "**📊 SCORE: 7/10**\nStrong commitment, add more context.",
    
    2: "**📊 SCORE: 7/10**\n\n**✅ STRENGTHS:** Committed, Active Listening\n**⚠️ GROWTH:** Specificity\n\nGood emotional choice. Add what specifically they're doing.",
    
    3: "**📊 SCORE: 7/10**\n\n**✅ STRENGTHS:**\n✓ Commitment — Fully invested\n✓ Active Listening — Built on offer\n✓ Group Mind — Focused on relationship\n\n**⚠️ GROWTH:**\n☐ Specificity — What exactly?\n☐ Game of Scene — Pattern unclear\n\n**💡 ANALYSIS:** You opened with emotional investment. Good! The opportunity is specificity. What specifically is happening?",
    
    4: "**📊 SCORE: 18/25**\n\n**BREAKDOWN:**\n• Commitment (5/5): Fully committed\n• Specificity (3/5): Good emotion, needs detail\n• Active Listening (5/5): Excellent\n• Game of Scene (3/5): Emerging\n• Group Mind (2/5): Self-focused\n\n**✅ WHAT YOU DID WELL:**\n✓ Never wavered\n✓ Acknowledged offer\n✓ Clear character POV\n\n**⚠️ TO IMPROVE:**\n☐ Concrete specificity — what happened?\n☐ Game identification — what's the pattern?\n\n**💡 COACHING:** Solid work. Add specifics. Make one specific choice before you speak.",
    
    5: "**📊 COMPREHENSIVE SCORE: 36/50**\n\n**🎭 COMMITMENT (8/10):** Very committed. Could add physical choices.\n\n**📍 SPECIFICITY (6/10):** Specific emotionally, vague situationally.\n\n**🎮 GAME (5/10):** Conflict established, pattern not clear.\n\n**👂 ACTIVE LISTENING (9/10):** EXCELLENT. You heard and responded perfectly.\n\n**🧠 GROUP MIND (3/10):** Your growth edge. Shift \"I express\" to \"We discover.\"\n\n**✅ YOUR GREATEST STRENGTHS:**\n✓ Active Listening\n✓ Commitment\n✓ Clear point of view\n\n**⚠️ GROWTH EDGES (priority):**\n1. Concrete Specificity\n2. Group Mind\n3. Game Identification\n\n**YOU'RE CLOSE TO BREAKTHROUGH. KEEP GOING.**"
}

# ============= USER SESSIONS =============
user_sessions = {}

def get_user_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "current_exercise": None,
            "current_scene": None,
            "feedback_level": 3
        }
    return user_sessions[user_id]

# ============= EMBEDS HELPER =============
def create_embed(title, description, color=0x5865f2):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="🤖 Improv Bot")
    return embed

# ============= BOT EVENTS =============
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is now running!")
    await bot.change_presence(activity=discord.Game(name="!improv help"))

# ============= COMMANDS =============
@bot.command(name='improv')
async def improv_menu(ctx):
    """Main menu for Improv Bot"""
    embed = create_embed(
        "🤖 IMPROV DECONSTRUCTION",
        "Select an exercise:\n\n"
        "**Exercise 1:** `!ex1` - Opening Scene\n"
        "**Exercise 2:** `!ex2` - Theme Naming\n"
        "**Exercise 3:** `!ex3` - Thematic Pitch\n"
        "**Exercise 4:** `!ex4` - Commentary\n"
        "**Exercise 5:** `!ex5` - The Gauntlet\n\n"
        "**Feedback:** `!feedback` - Get feedback levels\n"
        "**Help:** `!improv help` - Show all commands"
    )
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Show all available commands"""
    embed = create_embed(
        "📚 IMPROV BOT COMMANDS",
        "**Main Commands:**\n"
        "`!improv` - Show main menu\n"
        "`!ex1` - Opening Scene\n"
        "`!ex2` - Theme Naming (random scene)\n"
        "`!ex3` - Thematic Pitch (random scene)\n"
        "`!ex4` - Commentary (random scene)\n"
        "`!ex5` - The Gauntlet\n\n"
        "**Feedback System:**\n"
        "`!feedback` - Show feedback levels\n"
        "`!fb [1-5]` - Get feedback at level (1=minimal, 5=comprehensive)\n\n"
        "**Settings:**\n"
        "`!setfeedback [1-5]` - Set default feedback level"
    )
    await ctx.send(embed=embed)

@bot.command(name='ex1')
async def exercise1(ctx):
    """Exercise 1: Opening Scene"""
    embed = create_embed(
        "🔵 EXERCISE 1: OPENING SCENE",
        "**Prompt:** Kitchen\n\n"
        "Start the scene! Type your opening line.",
        color=0x3498db
    )
    await ctx.send(embed=embed)
    get_user_session(ctx.author.id)["current_exercise"] = 1

@bot.command(name='ex2')
async def exercise2(ctx):
    """Exercise 2: Theme Naming"""
    scene = random.choice(SCENES_2)
    get_user_session(ctx.author.id)["current_scene"] = scene
    
    embed = create_embed(
        "🟢 EXERCISE 2: THEME NAMING",
        f"**Scene:**\n{scene['text']}\n\n"
        f"**Themes to identify:**\n{scene['themes']}\n\n"
        "Analyze this scene and identify the themes!"
    )
    await ctx.send(embed=embed)

@bot.command(name='ex3')
async def exercise3(ctx):
    """Exercise 3: Thematic Pitch"""
    scene = random.choice(SCENES_3)
    get_user_session(ctx.author.id)["current_scene"] = scene
    
    embed = create_embed(
        "🟡 EXERCISE 3: THEMATIC PITCH",
        f"**Scene:**\n{scene['text']}\n\n"
        f"**Themes:**\n{scene['themes']}\n\n"
        "Pitch a different scene with these same themes!"
    )
    await ctx.send(embed=embed)

@bot.command(name='ex4')
async def exercise4(ctx):
    """Exercise 4: Commentary"""
    scene = random.choice(SCENES_4)
    get_user_session(ctx.author.id)["current_scene"] = scene
    
    embed = create_embed(
        "🟠 EXERCISE 4: COMMENTARY",
        f"**Scene:**\n{scene['text']}\n\n"
        f"**Themes:**\n{scene['themes']}\n\n"
        "Pitch 5 commentaries (2-3 logical, 2-3 absurd)!"
    )
    await ctx.send(embed=embed)

@bot.command(name='ex5')
async def exercise5(ctx):
    """Exercise 5: The Gauntlet"""
    embed = create_embed(
        "🔴 EXERCISE 5: THE GAUNTLET",
        "Run all exercises on your opening!\n\n"
        "Complete exercises 1-4 and report back when done.",
        color=0xe74c3c
    )
    await ctx.send(embed=embed)

@bot.command(name='feedback')
async def feedback_menu(ctx):
    """Show feedback level options"""
    embed = create_embed(
        "📊 FEEDBACK LEVELS",
        "**Choose a level:**\n"
        "`!fb 1` - Minimal feedback\n"
        "`!fb 2` - Basic feedback\n"
        "`!fb 3` - Standard feedback (default)\n"
        "`!fb 4` - Detailed feedback\n"
        "`!fb 5` - Comprehensive feedback\n\n"
        "**Example:** `!fb 5` to get comprehensive coaching"
    )
    await ctx.send(embed=embed)

@bot.command(name='fb')
async def show_feedback(ctx, level: int = None):
    """Show feedback at specified level"""
    if level is None:
        level = get_user_session(ctx.author.id)["feedback_level"]
    
    if level < 1 or level > 5:
        await ctx.send("❌ Feedback level must be between 1 and 5")
        return
    
    embed = create_embed(
        f"📊 FEEDBACK LEVEL {level}/5",
        FEEDBACK_LEVELS[level],
        color=0x43b581 if level >= 4 else 0xfaa61a
    )
    await ctx.send(embed=embed)

@bot.command(name='setfeedback')
async def set_feedback(ctx, level: int):
    """Set default feedback level"""
    if level < 1 or level > 5:
        await ctx.send("❌ Level must be between 1 and 5")
        return
    
    get_user_session(ctx.author.id)["feedback_level"] = level
    await ctx.send(f"✅ Default feedback level set to {level}")

@bot.command(name='complete')
async def complete_exercise(ctx):
    """Mark exercise as complete"""
    embed = create_embed(
        "✅ EXERCISE COMPLETE!",
        "What's next?\n\n"
        "`!feedback` - Get feedback\n"
        "`!improv` - Back to menu\n"
        "`!ex1` - Try another exercise"
    )
    await ctx.send(embed=embed)

# ============= RUN BOT =============
if __name__ == "__main__":
    BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
    bot.run(BOT_TOKEN)