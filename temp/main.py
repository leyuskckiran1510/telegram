from telegram import (
                        InlineQueryResultArticle,
                        ParseMode, 
                        InputTextMessageContent,
                        Update, 
                        LabeledPrice,
                        ShippingOption
                    )
from telegram.ext import (
                        Updater, 
                        InlineQueryHandler, 
                        CommandHandler, 
                        CallbackContext, 
                        MessageHandler,
                        Filters,
                        PreCheckoutQueryHandler,
                        ShippingQueryHandler
                        )
from telegram.utils.helpers import escape_markdown
from scrape import Run
import json
from uuid import uuid4

  
#5337004329:AAGi7x2DwRQrsWhD-EaYEzrHX1Lp9ReQ-TE   main token
#5343913274:AAEZLxQUdfVWbtIr-vfl40znbpps3ubqzkk   testing token
updater = Updater("5343913274:AAEZLxQUdfVWbtIr-vfl40znbpps3ubqzkk",
                  use_context=True)
  
b= Run()
def start(update, context):
    global b
    b = Run()
    print(update.message.from_user['id'],update.message.from_user['name'],"Start")
    update.message.reply_text(
        f"Welcome To downloder{update.message.from_user['name']}.\n\nAvailable Commands :-\
    /generate - To choose the youtube quality and content Type\
    /link x,y - To get the choosen link\
    example :- /link 0,1  (link of '0' meaning video and '1' meaning second higest quality.)")
  
def help(update, context):
    print(update.message.from_user['id'],update.message.from_user['name'],"Help")
    update.message.reply_text("""Available Commands :-
    /generate - To choose the youtube quality and content Type
    /link x,y - To get the choosen link
    example :- /link 0,1  (link of '0' meaning video and '1' meaning second higest quality.)""")
  
  
def generate(update, context,redirect=False):

    print(update.message.from_user['id'],update.message.from_user['name'],"Generate",context.args)
    name = update.message.from_user['id']
    if not redirect:
        url =context.args
        if len(url)<1:
            update.message.reply_text("Please Provide URl "+"\n\nAvailable Commands :-\n \
        /generate - To choose the youtube quality and content Type\n\
        /link x,y - To get the choosen link\n\
        example :- /link 0,1  (link of '0' meaning video and '1' meaning second higest quality.)")
            return
    else:
        url=[update.message.text]

    c  = b.urls(url[0])
    with open(f'{name}.json','w') as fl:
        fl.write(str(c).replace('\'','"'))
    if 'error' not in c.keys():
        quality = ''
        for n,i in enumerate(c.keys()):
            quality+=f'[+] {i}\n'+'\n'.join([f"[-] ({n},{m}) {j}" for m,j in enumerate(c[i].keys())])+'\n'

        
        update.message.reply_text(quality+"\n\nAvailable Commands :-\n\
        /generate - To choose the youtube quality and content Type\n\
        /link x,y - To get the choosen link\n\
        example :- /link 0,1  (link of '0' meaning video and '1' meaning second higest quality.)")
    else:
        update.message.reply_text(c['error']+"\n\nAvailable Commands :-\n \
    /generate - To choose the youtube quality and content Type\n\
    /link x,y - To get the choosen link\n\
    example :- /link 0,1  (link of '0' meaning video and '1' meaning second higest quality.)")


def link(update,context):
    cv  = context.args
    print(update.message.from_user['id'],update.message.from_user['name'],"Link",cv)
    try:
        x,y = cv[0].split(",")
        x, y =int(x),int(y)
        with open(f"{update.message.from_user['id']}.json",'r') as file:
            url=json.load(file)
        final = url[list(url.keys())[x]][list(url[list(url.keys())[x]].keys())[y]]
        update.message.reply_text(final)
    except:
        update.message.reply_text("Please Type /help for help . The format you provided was in correct.")
   
  
def unknown(update, context):
    a =update.message.text
    if "https://" in a:
        generate(update,context,redirect=True)
        return
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)
  
  
def unknown_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)



def inlinequery(update, context):
    """Handle the inline query."""
    query = update.inline_query.query
    with open("IlineQueriesFromUser.txt","a") as fl:
        cv = f"({update.inline_query.from_user['id']}) {update.inline_query.from_user['id']} => {query} \n"
        fl.write(cv)
    print(query)
    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Generate-link",
            input_message_content=InputTextMessageContent(str(b.urls(query,inline=True))),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Help",
            input_message_content=InputTextMessageContent("You can goto offical bot page and generate link with different video quality\
                and manymore but this inline generate call will only provide you with a single link for each video and audio.\
                just invoke the bot and type the url and select 'Generate-link' in the pop up. That's it."),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Start",
            input_message_content=InputTextMessageContent("start"),
        ),
    ]
    #b = generate(update,context,inline=True)
    update.inline_query.answer(results)


def payment(update, context):
    """Sends an invoice with shipping-payment."""
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "TestServer"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    provider_token = "2edf4362ce45850f37323ad8e09a07695404756b:qwerty"
    currency = "USD"
    # price in dollars
    price = 1
    # price * 100 so as to include 2 decimal points
    # check https://core.telegram.org/bots/payments#supported-currencies for more details
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        provider_token,
        currency,
        prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )
def shipping_callback(update, context):
    """Answers the ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
        return

    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)])]
    # second option has an array of LabeledPrice objects
    price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
    options.append(ShippingOption('2', 'Shipping Option B', price_list))
    query.answer(ok=True, shipping_options=options)


def precheckout_callback(update, context):
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)

def successful_payment_callback(update, context):
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    update.message.reply_text("Thank you for your payment!")
  

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('generate', generate))
dispatcher.add_handler(CommandHandler("Upgrade", payment))
dispatcher.add_handler(CommandHandler('link', link))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(MessageHandler(Filters.text, unknown))
dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))
dispatcher.add_handler(InlineQueryHandler(inlinequery))
dispatcher.add_handler(ShippingQueryHandler(shipping_callback))
dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
updater.start_polling()
updater.idle()
