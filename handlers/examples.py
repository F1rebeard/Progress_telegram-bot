progress_sub_messages = {
                'standard_thirty_days_sub':(
                    '1',
                    'dva'
                ),
                'plus_coach_thirty_days_sub':(
                    'adin', 'dvau'
                )
            }

print(progress_sub_messages.get('standard_thirty_days_sub')[0])
print(type(progress_sub_messages.get('standard_thirty_days_sub')[1]))
