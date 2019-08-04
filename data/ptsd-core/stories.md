## welcome
* greet
  - utter_greet
  - utter_intro
  - utter_continue_prompt
> check_answered_prompt

## does not want to continue
> check_answered_prompt
* deny
 - utter_undertand_does_not_want_help
 - utter_referral
 - action_restart

## wants to continue
> check_answered_prompt
* affirm
 - utter_get_started
 - utter_question_1
> check_answered_question_1

## second question
> check_answered_question_1
* affirm
  - utter_sorry_to_hear
  - utter_question_2

## deny first question
> check_answered_question_1
* deny
  - utter_sorry_cannot_help
  - utter_referral
  - action_restart

## referral
* human_handoff
  - utter_sorry_cannot_help
  - utter_referral
  - action_restart

## say goodbye
* goodbye
  - utter_goodbye
  - action_restart
