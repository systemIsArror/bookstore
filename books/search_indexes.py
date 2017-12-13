from haystack import indexes
from books.models import Books

#指定对于模型类的某些数据建立索引，　一般类名：模型类名+index
class BooksIndex(indexes.SearchIndex, indexes.Indexable):
	#指定根据表中的那些字段建立索引：比如：商品名称，商品描述
	text = indexes.CharField(document=True, use_template=True)

	def get_model(self):
		return Books

	def index_queryset(self, using=None):
		return self.get_model().objects.all()

