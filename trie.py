import functools

class Trie(object):
    def __init__(self):
        self.children = {}
        self.flag = False
        self.obj = list()

    def add(self, char):
        self.children[char] = Trie()

    def insert(self, word, name):
        node = self
        for char in word:
            if char not in node.children:
                node.add(char)
            node = node.children[char]
        node.flag = True
        node.obj.append(name)

    def search_names(self, prefix, final, i = 0):
        results = list()
        data = {'rank':i+1}
        i += 1
        if self.flag:
            results = self.obj
            results.sort(key = lambda s: len(s))

        data['result'] = results
        final.append(data)
        if not self.children: return data
        for (char, node) in self.children.items():
            result = node.search_names(prefix + char, final, i)
            i += 1
        return data

    def autocomplete(self, phrase):
        results = {'matched':[],'suggestions':[]}
        for prefix in phrase.split(' '):
            node = self
            for char in prefix:
                if char not in node.children:
                    break
                node = node.children[char]
            final = []
            
            node.search_names(prefix,final)
            for data in final:
                if 1 == data['rank']:
                    results['matched'] += data['result']
                    results['matched'].sort(key = lambda s: len(s))
                else:
                    results['suggestions'] += data['result']
                    results['suggestions'].sort(key = lambda s: len(s))
        final = []
        for r in results['matched'] + results['suggestions']:
            seq = r.lower().strip().replace(" ", "%20")
            if phrase == seq:
                final.insert(0, {'name':r})
            else:
                final.append({'name':r})
        return final
