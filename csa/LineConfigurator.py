import math
class LineConfigurator:
    def __init__(self,types):
        self.types = types
        self.typeList = self.unique_elements()
        self.lineLengths = self.count_types()
        self.currentLineLen = self.initalLineLen()
        self.rowLengths = self.calc_rowLengths()
        self.breakPoints = self.calcLineBreakPoints()

        print(self.lineLengths)
        print(self.rowLengths)
        print(self.breakPoints)
    
        

    def moveToEnd(self,type): 
        # For first row, move upwards
        curLineLen = self.currentLineLen[type]
        typeBreakPoints = self.breakPoints[type]

        if(self.lineLengths[type] < 6): 
            self.currentLineLen[type] += 1
            return(3,curLineLen)

        leftPartSize = self.lineLengths[type]-typeBreakPoints[2]
        leftRowLen = round(math.sqrt(leftPartSize))

        if(curLineLen < typeBreakPoints[0]): 
            self.currentLineLen[type] += 1
            return(3,curLineLen)
        elif (curLineLen < (typeBreakPoints[1])): 
            moveInstructions = self.moveDownLine(type)
            self.currentLineLen[type] += 1
            return moveInstructions
        elif (curLineLen < typeBreakPoints[2]): 
            moveInstructions = self.moveUpLine((curLineLen-typeBreakPoints[1]),type)
            self.currentLineLen[type] += 1
            return moveInstructions
        else: 
            moveInstructions = self.moveLeftLine((curLineLen-typeBreakPoints[2]),leftRowLen)
            self.currentLineLen[type] += 1
            return moveInstructions

    def moveDownLine(self,type): 
        rowNum = math.ceil((self.currentLineLen[type]+1)/self.rowLengths[type])
        rowIndex = (self.currentLineLen[type] % self.rowLengths[type])
        count = rowNum + (self.rowLengths[type]-rowIndex) -1
        return (2,count)
    
    def moveUpLine(self,currentLineLen,type): 
        rowNum = math.floor(currentLineLen/self.rowLengths[type])
        rowIndex = self.rowLengths[type]-(currentLineLen % self.rowLengths[type])
        count = rowNum + rowIndex
        return (3,count)
    
    def moveLeftLine(self,currentLineLen,leftRowLen): 
        rowNum = math.floor(currentLineLen/leftRowLen)
        rowIndex = leftRowLen-(currentLineLen % leftRowLen)
        if(rowNum < 2): 
            return (2,rowIndex)
        else: 
            return (2,rowNum + rowIndex -1)

    def calc_rowLengths(self): 
        rowLengths = {}
        for type in self.types: 
            rowLengths[type] = self.calcRowLen(self.lineLengths[type])
        return rowLengths

    def calcRowLen(self,size):
        k = round(size/3) 
        return round(math.sqrt(k))

    def unique_elements(self): 
        unique_set = set(self.types)
        unique_list = list(unique_set)
        return unique_list
    
    def initalLineLen(self): 
        initLineLen = {}
        for element in self.typeList:
            initLineLen[element] = 1
        return initLineLen
    
    def count_types(self):
        element_counts = {}
        for element in self.types:
            if element in element_counts:
                element_counts[element] += 1
            else:
                element_counts[element] = 1
        return element_counts
    
    def calcLineBreakPoints(self): 
        lineBreakPoints = {}
        for type in self.types: 
            lineBreakPoints[type] = self.calcTypeBreakPoints(self.rowLengths[type],self.lineLengths[type])
        return lineBreakPoints

    def calcTypeBreakPoints(self,rowLen,typeSize):
        k = round(typeSize/3)
        return [rowLen,k+rowLen,2*k+rowLen]