class Resource:
    __wood: float
    __gold: float
    __food: float

    def __init__(self, wood: float, gold: float, food: float):
        assert wood >= 0,"wood:"+ str(wood)
        assert gold >= 0,"gold:" + str(gold)
        assert food >= 0,"food:" + str(food)
        self.__wood = wood
        self.__gold = gold
        self.__food = food

    def get_wood(self) -> float:
        return self.__wood
    
    def get_gold(self) -> float:
        return self.__gold
    
    def get_food(self) -> float:
        return self.__food
    
    def add_wood(self,value : float) :
        assert value >= 0, value
        self.__wood += value

    def add_gold(self,value : float) :
        assert value >= 0, value
        self.__gold += value

    def add_food(self,value : float) :
        assert value>=0,value
        self.__food += value

    def remove_wood(self,value : float) :
        assert self.__wood >= value >= 0,value
        self.__wood -= value

    def remove_gold(self,value : float) :
        assert self.__gold >= value >= 0,value
        self.__gold -= value

    def remove_food(self,value : float) :
        assert self.__food >= value >= 0,value
        self.__food -= value