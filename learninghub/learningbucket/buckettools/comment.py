#
# Comment tools
# 
import learningbucket.models

# return a list of tags based on a comment string
def filterTags(commentString):
    taglist = []
    words = commentString.split()
    for word in words:
        if len(word) > 1 and word[0] == "#":
            taglist.append(word)

    return taglist

def storeTags(taglist=[], project=None):

    if(project == None):
        print("storeTags tried can not store to project None")
        return False

    for tag in taglist:
        m = learningbucket.models.EProjectTag(project=project,tag=tag)
        m.save()

    return True

#
# Run som tests
#
if __name__ == "__main__":
    teststring = "This is a #comment\n A new #tag is on the #way"
    print(filterTags(teststring))
