# Alarm status codes, using constants instead of Enum for ease of autocomplete
ACTIVE = 'active'
RINGING = 'ringing'
DISABLED = 'disabled'

# Alarm modes
NO_ALARM = 'no_alarm'
QUE_SERA_SERA = 'que_sera_sera'
BASIC = 'basic'
PASSIVE_AGGRESSIVE = 'passive_aggressive'
AT_ALL_COSTS = 'at_all_costs'

# Alarm hierarchy
MODE_DEGREE = {
    NO_ALARM: 0,
    QUE_SERA_SERA: 1,
    BASIC: 2,
    PASSIVE_AGGRESSIVE: 3,
    AT_ALL_COSTS: 4
}

# Mapping of event importance to alarm mode
EVENT_MODE = {'high': AT_ALL_COSTS, 'medium': PASSIVE_AGGRESSIVE, 'low': BASIC, 'zero': QUE_SERA_SERA}
