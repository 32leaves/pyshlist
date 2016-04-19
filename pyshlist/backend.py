import tinydb

class Purchases(object):
    """Manages all purches in the database"""
    
    def __init__(self, db):
        self.db = db.table('purchases')
        
    @property
    def all(self):
        return self.db.all()
        
    def new(self, name, price, due_date, desirability = 0, category = None, description = None):
        """Creates a new purchase"""
        doc = {
            "name" : name,
            "price" : price,
            "desirability" : desirability,
            "due_date" : due_date,
            "category" : category,
            "description" : description
        }
        self.db.insert(doc)
        
    def remove(self, name):
        """Removes a purchase with a given name"""
        Purchase = tinydb.Query()
        removed_items = self.db.remove(Purchase.name == name)
        return any(removed_items)
        
    def set_desirability(self, name, desirability):
        """Sets the desirability of a purchase"""
        Purchase = tinydb.Query()
        updated_items = self.db.update({ 'desirability' : desirability }, Purchase.name == name)
        return any(updated_items)
    
    @property    
    def categories(self):
        return set([ x['category'] for x in self.db.all() if not x['category'] is None ])
        
        
class Comparisons(object):
    
    def __init__(self, db):
        self._db = db
        self._table = db.table('comparisons')
    
    def vote(self, a, b, a_more_important):
        """Marks the first purchase name as more important than the other"""
        self._table.insert({
            "a" : a,
            "b" : b,
            "a_more_important": a_more_important
        })
        

    def get_score(self, purchase_name):
        """Returns the score (0: not important to 1: very important) of a purchase based on prior comparisons"""
        Comparison = tinydb.Query()
        comparisons_won = 0
        comparisons_won += self._table.count((Comparison.a == purchase_name) & (Comparison.a_more_important == True))
        comparisons_won += self._table.count((Comparison.b == purchase_name) & (Comparison.a_more_important == False)) 
        comparisons_involved = (self._table.count(Comparison.a == purchase_name) + self._table.count(Comparison.b == purchase_name))
        
        result = None
        if comparisons_involved > 0:
            result = float(comparisons_won) / float(comparisons_involved)
        return result
        

    def prune(self, valid_purchase_names = None):
        """Removes all comparisons which contain non-valid purchase names"""
        if valid_purchase_names is None:
            purchases = Purchases(self._db)
            valid_purchase_names = [ p['name'] for p in purchases.all ]
        
        Comparison = tinydb.Query()
        self._table.remove(Comparison.a.test(lambda x: not x in valid_purchase_names))
        self._table.remove(Comparison.b.test(lambda x: not x in valid_purchase_names))
    
    
    @property    
    def missing_comparisons(self):
        """Returns all missing purchase comparisons"""
        purchases = [ p['name'] for p in Purchases(self._db).all ]
        all_comparisons = [ (purchases[i], purchases[j]) for i in range(len(purchases)) for j in range(i) ]
        
        Comparison = tinydb.Query()
        return [ x for x in all_comparisons if self._table.count(((Comparison.a == x[0]) & (Comparison.b == x[1])) | ((Comparison.a == x[1]) & (Comparison.b == x[0]))) == 0 ]

    @property
    def rated_purchases(self):
        """Returns a list of all purchases with their score added"""
        #self.prune()
        
        purchases = Purchases(self._db).all
        for p in purchases:
            p['desirability'] = self.get_score(p['name'])
        return purchases
