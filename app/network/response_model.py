import json

class ResponseModel:

    def __init__(self, status=0, message="", data=None):
        self.status = status
        self.message = message
        self.data = data

    def jsonSerialize(self):
        try:
            return json.dumps(self, default=self.toDictionay)
        except Exception as ex:
            print(ex)
            return ""

    def toDictionay(self, obj):
        data = {}
        if not obj.data:
            data = {}
        else:
            try:
                data = obj.data.__dict__
            except Exception as ex:
                data = obj.data

        return {
            'status': obj.status,
            'message': obj.message,
            'data': data
        }


class B:
    name = ""
    def __init__(self):
        self.name = "123"

class A:
    status = 0
    message = "123aaa"
    def __init__(self):
        self.data = B()

    def jsonSerialize(self):
        try:
            return json.dumps(self, default=self.toDictionay)
        except Exception as ex:
            print(ex)
            return ""

    def toDictionay(self, obj):
        return {
            'status': obj.status,
            'message': obj.message,
            'data': obj.data.__dict__
        }

def main():
    # a = A()
    # str = a.jsonSerialize()
    result = BaseResponse(0, "12345")
    str = result.jsonSerialize()
    print("-----")
    print(str)

if __name__ == "__main__":
    main()