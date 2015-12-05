# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# 	 http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from json import dumps

from pyspark.rdd import RDD

from .types import as_java_object


class EsJsonRDD(RDD):
	def __init__(self, ctx, resource=None, query=None, **kwargs):
		kwargs = as_java_object(ctx._gateway, kwargs)
		jrdd = _helper(ctx).esJsonRDD(ctx._jsc, resource, query, kwargs)
		super(EsJsonRDD, self).__init__(jrdd, ctx)


def saveToEs(rdd, resource=None, **kwargs):
	rdd = rdd.map(dumps)
	kwargs = as_java_object(rdd.ctx._gateway, kwargs)
	_helper(rdd.ctx).saveJsonToEs(rdd._jrdd, resource, kwargs)

def saveJsonToEs(rdd, resource=None, **kwargs):
	kwargs = as_java_object(rdd.ctx._gateway, kwargs)
	_helper(rdd.ctx).saveJsonToEs(rdd._jrdd, resource, kwargs)


def _helper(ctx):
	return ctx._jvm.java.lang.Thread.currentThread().getContextClassLoader() \
		.loadClass("pyspark_elastic.PythonHelper").newInstance()