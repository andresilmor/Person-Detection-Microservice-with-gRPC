def prepareQuery(parent, selected_fields, returnAs):
    queryFilter = ' UNWIND apoc.any.properties(' + parent + ',['
    childs = []
    for field in selected_fields:
       
        for selection in field.selections:
            if len(selection.selections) == 0:
                queryFilter += (', \"' + selection.name + '\"')
            else:
                childs.append(selection)

    queryFilter += (']) AS ' + returnAs + ' ')

    for index in range(len(childs)):
        newFilter, newReturn = prepareQuery(childs[index].name,[childs[index]], str(childs[index].name).capitalize())
        queryFilter += newFilter
        returnAs += (', ' + newReturn)

    return queryFilter, returnAs