import  uuid
from    enum    import  Enum,auto
from    anytree import Node, RenderTree

class   BuildParentChildRelation():

    def __init__(self):
        self.ParentID=uuid.uuid4()
        self.ChildID=None

    def swapParentAndChildRelation(self,StageCount):
        if(StageCount==0 or StageCount==1):
            pass
        else:
            temp=self.ParentID       #redundant. Not required.     
            self.ParentID=self.ChildID
            self.ChildID=uuid.uuid4()









