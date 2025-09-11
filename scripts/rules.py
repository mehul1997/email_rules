import json
import email.utils as e_utils
from datetime import datetime

def load_rules():
    with open('../data/rules.json', 'r') as f:
        return json.load(f)


def apply_rules(email, rules):
    conditions_met = []

    for rule in rules['rules']:
        field_value = email.get(rule['field'])
        predicate = rule['predicate']
        rule_value = rule['value']

        if field_value is None:
            conditions_met.append(False)
            continue

        if rule['field'] == 'date':
            email_date = e_utils.parsedate_to_datetime(field_value)
            rule_date = datetime.strptime(rule_value, '%Y-%m-%d')

            timestamp1 = email_date.timestamp()
            timestamp2 = rule_date.timestamp()

            if predicate == 'less_than':
                conditions_met.append(timestamp1 < timestamp2)
            elif predicate == 'greater_than':
                conditions_met.append(timestamp1 > timestamp2)
        else:
            if predicate == 'contains':
                conditions_met.append(rule_value.lower() in field_value.lower())
            elif predicate == 'does_not_contain':
                conditions_met.append(rule_value.lower() not in field_value.lower())
            elif predicate == 'equals':
                conditions_met.append(rule_value.lower() == field_value.lower())
            elif predicate == 'does_not_equal':
                conditions_met.append(rule_value.lower() != field_value.lower())

    if rules['predicate'] == 'All':
        return all(conditions_met)
    else:
        return any(conditions_met)



def main():
    rules = load_rules()
    print(rules)

if __name__=='__main__':
    main()