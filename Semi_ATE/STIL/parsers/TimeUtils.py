# -*- coding: utf-8 -*-

class TimeUtils:
    
    
    def bodmas(data, time_expr):
        
#        print(f"bodmas input {data}")

        # Search for brackets
        start_brackets = []
        end_brackets = []
        
        index = 0
        for item in data:
            if item == '(':
                start_brackets.append(index)
            elif item == ')':
                end_brackets.append(index)
            index += 1
            
        sb = len(start_brackets)
        eb = len(end_brackets)
        
        if (sb > 0 or eb > 0) and sb != eb:
            err_msg = f"No matching brаckets for time expression {time_expr}!"
            raise Exception(err_msg)
        elif sb > 0 and eb > 0:
            for i in range(sb):
                sbi = start_brackets[i]
                ebi = end_brackets[i]
                sub_data = []
                for di in range(sbi+1, ebi):
                    d = data[di]
                    sub_data.append(d)
                val = TimeUtils.bodmas(sub_data, time_expr)
                
#                print(f"bodmas after recursive () {val}")
                
#                print(f"bodmas before substitution () {data}")
                insert = sbi
                del data[sbi:ebi+1]
                data.insert(insert, str(val))
#                print(f"bodmas after substitution () {data}")

#        print(f"bodmas after () {data}")

        div = []
        
        index = 0
        for item in data:
            if item == '/':
                div.append(index)
            index += 1
        
        if len(div) > 0:
            for i in range(len(div)):
                
                left  = data[div[i]-1]
                right = data[div[i]+1]
                
                # Two cases:
                # Numeric / Frequency
                # Time / Numeric

                try:
                    left_value = float(left)
                    freq = TimeUtils.get_freq_Hz(right)
                    if freq != None:
                        result = left_value / freq * 1E15
                    else:
                        err_msg = f"Expecting frequency value for the right operand, but got '{right}' in time expression '{time_expr}'!"
                        raise Exception(err_msg)
                except:
                    try:
                        right_value = float(right)
                        left_value = TimeUtils.get_time_fsec(left)
                        result = left_value / right_value
                    except:
                        err_msg = f"Expecting either numeric value for the left or right operand, but got left '{left}' and right '{right}' in time expression '{time_expr}'!"
                        raise Exception(err_msg)
                
                insert = div[i]-1
                del data[div[i]-1:div[i]+2]
                data.insert(insert, str(int(result)) + "fs")
                
#        print(f"bodmas after / {data}")
                    
        mul = []
        
        index = 0
        for item in data:
            if item == '*':
                mul.append(index)
            index += 1
                
        if len(mul) > 0:
            for i in range(len(mul)):
                
                left  = data[mul[i]-1]
                right = data[mul[i]+1]
                
                left_value = TimeUtils.get_time_fsec(left)
                right_value = TimeUtils.get_time_fsec(right)
                
                is_right_value_time = True
                
                if left_value == None:
                    try:
                        float(left)
                    except:
                        err_msg = f"Expecting time or numeric value for the left operand, but got '{left}' in time expression '{time_expr}'!"
                        raise Exception(err_msg)
                elif right_value == None:
                    try:
                        right_value = float(right)
                        is_right_value_time = False
                    except:
                        err_msg = f"Expecting time or numeric value for the right operand, but got '{right}' in time expression '{time_expr}'!"
                        raise Exception(err_msg)
                
                if is_right_value_time:
                    result = left_value * right_value / 1E6
                else:
                    result = left_value * right_value

                insert = mul[i]-1
                del data[mul[i]-1:mul[i]+2]
                data.insert(insert, str(int(result)) + "fs")
                
#        print(f"bodmas after * {data}")

        add = []
        
        index = 0
        for item in data:
            if item == '+':
                add.append(index)
            index += 1

        if len(add) > 0:
            for i in range(len(add)):
                
                left  = data[add[i]-1]
                right = data[add[i]+1]
                
                left_value = TimeUtils.get_time_fsec(left)
                right_value = TimeUtils.get_time_fsec(right)
                
                if left_value == None:
                    err_msg = f"Expecting time value for the left operand, but got '{left}' in time expression '{time_expr}'!"
                    raise Exception(err_msg)
                elif right_value == None:
                    err_msg = f"Expecting time value for the right operand, but got '{right}' in time expression '{time_expr}'!"
                    raise Exception(err_msg)
                
                result = left_value + right_value
                insert = add[i]-1
                del data[add[i]-1:add[i]+1]
                data.insert(insert, str(int(result)) + "fs")

#        print(f"bodmas after - {data}")

        sub = []
        
        index = 0
        for item in data:
            if item == '-':
                sub.append(index)
            index += 1

        if len(sub) > 0:
            for i in range(len(sub)):
                left  = data[sub[i]-1]
                right = data[sub[i]+1]
                
                left_value = TimeUtils.get_time_fsec(left)
                right_value = TimeUtils.get_time_fsec(right)
                
                if left_value == None:
                    err_msg = f"Expecting time value for the left operand, but got '{left}' in time expression '{time_expr}'!"
                    raise Exception(err_msg)
                elif right_value == None:
                    err_msg = f"Expecting time value for the right operand, but got '{right}' in time expression '{time_expr}'!"
                    raise Exception(err_msg)
                
                result = left_value - right_value
                insert = sub[i]-1
                del data[sub[i]-1:sub[i]+1]
                data.insert(insert, str(int(result)) + "fs")

#        print(f"bodmas after + {data}")
#        print(f"bodmas return {data}")
        
        if data[0].endswith('fs'):
            return data[0]
        else:
            fsec = TimeUtils.get_time_fsec(data[0])
            return str(int(fsec)) + "fs"

    def get_freq_Hz(expr):
        
        v = expr.strip()
        if v.endswith('Hz'):
            
            if v.endswith('aHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value/1000000000000000000.0
            elif v.endswith('fHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value/1000000000000000.0
            elif v.endswith('pHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value/1000000000000.0
            elif v.endswith('nHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value/1000000000.0
            elif v.endswith('uHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value/1000000.0
            elif v.endswith('mHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value/1000.0

            elif v.endswith('kHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value*1000.0
            elif v.endswith('MHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value*1000000.0
            elif v.endswith('GHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value*1000000000.0
            elif v.endswith('THz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value*1000000000000.0
            elif v.endswith('PHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value*1000000000000000.0
            elif v.endswith('EHz'):
                v_str = v[0:len(v)-3]
                value = float(v_str)
                return value*1000000000000000000.0
            else:
                # Hz
                v_str = v[0:len(v)-1]
                value = float(v_str)
                return value
        else:
            return None



    def get_time_fsec(expr):
        
        v = expr.strip()
        if v[0] == "'":
            v = v[1:len(v)]
        
        if v[-1] == "'":
            v = v[0:-1]
            
        if v.endswith('s'):
            
            if v.endswith('as'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value/1000
            elif v.endswith('fs'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value
            elif v.endswith('ps'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000
            elif v.endswith('ns'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000
            elif v.endswith('us'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000000
            elif v.endswith('ms'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000000000

            elif v.endswith('ks'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000000000000000
            elif v.endswith('Ms'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000000000000000000
            elif v.endswith('Gs'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000000000000000000000
            elif v.endswith('Ts'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000000000000000000000000
            elif v.endswith('Ps'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000000000000000000000000000
            elif v.endswith('Es'):
                v_str = v[0:len(v)-2]
                value = float(v_str)
                return value*1000000000000000000000000000000000
            else:
                # seconds
                v_str = v[0:len(v)-1]
                value = float(v_str)
                return value*1000000000000000
        else:
            return None
