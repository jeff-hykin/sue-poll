

poll = {
    "letter_options" : [],
    "poll["options"]" : []
    "question" : "",
    "poll":{}
}

def poll(textBody):
    """!poll <name/question>\n-<option1>  \n-<option2> ... \n<option n>"""
    global poll
    
    options = textBody.split('\n-') # FIXME, not sure if options would include the 'poll' or '!poll' 
    
    # get the poll question 
    poll["question"] = options.pop(0)
    # get the poll options 
    poll["options"] = options 
    # reset the last poll and replace it with a new poll 
    poll["letter_options"] = []
    poll["vote_tracker"] = {}
    # create the output to display 
    output_ = poll["question"] + "\n"
    # regenerate variables that will display the poll["options"] 
    index_ = 64 # start right before the ASCII 'A' 
    for each_option in poll["options"]:
        index_ += 1
        option_letter = char(index_) 
        poll["letter_options"].append(option_letter) 
        poll["vote_tracker"][option_letter] = set()
        output_ += "\n"+option_letter+". "+each_option

    rprint(output_)

    
        
def vote(textBody,sender):
    """!vote <letter>"""
    global poll
    options = textBody.split(' ')  # FIXME, not sure if poll["options"] would include the 'vote' or '!vote' 
    
    # if there is actually a correct input
    if len(options) == 1:
        the_letter = options[0].upper()
        # if the letter is one of the poll["options"]
        if the_letter in poll["letter_options"]:
            # then add the sender to that vote
            poll["vote_tracker"][the_letter].add(sender)
    
    # display the new status
    output_ = poll["question"] + "\n"
    index_ = 64 # start right before the ASCII 'A' 
    for each_option in poll["options"]:
        index_ += 1
        option_letter = char(index_) 
        number_of_votes = len(poll["vote_tracker"][option_letter])
        output_ += "\n("+ str(number_of_votes) +" votes) "+option_letter+". "+each_option

    rprint(output_)
