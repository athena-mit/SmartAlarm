class VirtualRoom:
    __LIGHTING_OPTIONS = ['#000000', '#4d4d00', '#999900', '#e6e600', '#ffff33']
    __brightness = 0

    def get_brightness(self):
        return self.__LIGHTING_OPTIONS[self.__brightness]

    def increase_brightness(self):
        if self.__brightness < len(self.__LIGHTING_OPTIONS) - 1:
            self.__brightness += 1
        return self.__LIGHTING_OPTIONS[self.__brightness]

    def max_brightness(self):
        self.__brightness = len(self.__LIGHTING_OPTIONS) - 1
        return self.__LIGHTING_OPTIONS[self.__brightness]
