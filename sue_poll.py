poll_data = {
    "letter_options" : [],
    "options" : [],
    "question" : "",
    "poll":{}
}
@bp.route('/poll')
def poll():
    """!poll <name/question>\n-<option1>  \n-<option2> ... \n<option n>"""
    global poll_data
    
    textBody = msg.textBody
    sender = msg.buddyId

    options = textBody.split('\n-') # FIXME, not sure if options would include the 'poll' or '!poll' 
    
    # get the poll question 
    poll_data["question"] = options.pop(0)
    # get the poll options 
    poll_data["options"] = options 
    # reset the last poll and replace it with a new poll 
    poll_data["letter_options"] = []
    poll_data["vote_tracker"] = {}
    # create the output to display 
    output_ = poll_data["question"] 
    # regenerate variables that will display the poll_data["options"] 
    index_ = 64 # start right before the ASCII 'A' 
    for each_option in poll_data["options"]:
        index_ += 1
        option_letter = chr(index_) 
        poll_data["letter_options"].append(option_letter) 
        poll_data["vote_tracker"][option_letter] = set()
        output_ += "\n"+option_letter+". "+each_option

    return output_

@bp.route('/vote')
def vote():
    """!vote <letter>"""
    global poll_data

    textBody = msg.textBody
    sender = msg.buddyId

    options = textBody.split(' ')  # FIXME, not sure if poll_data["options"] would include the 'vote' or '!vote' 
    
    # if there is actually a correct input
    if len(options) == 1:
        the_letter = options[0].upper()
        # if the letter is one of the poll_data["options"]
        if the_letter in poll_data["letter_options"]:
            # remove their vote from all options 
            for each in poll_data["letter_options"]:
                # if their vote is in the set 
                if sender in poll_data["vote_tracker"][each]:
                    # then remove it
                    poll_data["vote_tracker"][each].remove(sender)
            # then add the sender to the one the just recently voted for
            poll_data["vote_tracker"][the_letter].add(sender)
    
    # display the new status
    output_ = poll_data["question"]
    index_ = 64 # start right before the ASCII 'A' 
    for each_option in poll_data["options"]:
        index_ += 1
        option_letter = chr(index_) 
        number_of_votes = len(poll_data["vote_tracker"][option_letter])
        output_ += "\n("+ str(number_of_votes) +" votes) "+option_letter+". "+each_option

    return output_
