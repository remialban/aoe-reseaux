class Resource:
    __wood: int
    __gold: int
    __food: int

    def __init__(self, wood: int, gold: int, food: int):
        assert wood >= 0,"wood:"+ str(wood)
        assert gold >= 0,"gold:" + str(gold)
        assert food >= 0,"food:" + str(food)
        self.__wood = wood
        self.__gold = gold
        self.__food = food

    def get_wood(self) -> int:
        return self.__wood
    
    def get_gold(self) -> int:
        return self.__gold
    
    def get_food(self) -> int:
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