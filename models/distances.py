import tensorflow as tf
from tensorflow import keras

class Euclidean_Distance(keras.layers.Layer):
    def __init__(self,**kwargs):
        super(Euclidean_Distance,self).__init__(**kwargs)
        #self.constant = tf.Variable(initial_value=0.1, dtype=tf.float32, trainable=True)

    def call(self,inputs,**kwargs):
        support,query = inputs
        #print(query.shape)
        #print(v.shape)
        q2 = tf.reduce_sum(query ** 2, axis=1, keepdims=True)
        s2 = tf.reduce_sum(support ** 2, axis=1, keepdims=True)
        qdots = tf.matmul(query, tf.transpose(support))
        return  -(tf.sqrt(q2 + tf.transpose(s2) - 2 * qdots))
        #return  -(self.constant * (q2 + tf.transpose(s2) - 2 * qdots))
        #return  -((q2 + tf.transpose(s2) - 2 * qdots))
    
    def compute_output_shape(self,input_shape):
        return tf.TensorShape(input_shape[:-1])
    
    def get_config(self):
        config = super(Euclidean_Distance,self).get_config()
        return config

class Cosine_Distance(keras.layers.Layer):
    def __init__(self,**kwargs):
        super(Cosine_Distance,self).__init__(**kwargs)
        #self.constant = tf.Variable(initial_value=0.1, dtype=tf.float32, trainable=True)
    def call(self,inputs,**kwargs):
        support,query = inputs
        support = tf.nn.l2_normalize(support,axis=1)
        query = tf.nn.l2_normalize(query,axis=1)
        distance = 1 - tf.matmul(query, support,transpose_b=True)
        return  (distance)
    
    def compute_output_shape(self,input_shape):
        return tf.TensorShape(input_shape[:-1])

    def get_config(self):
        config = super(Cosine_Distance,self).get_config()
        return config

class Mahalanobis_Distance(keras.layers.Layer):
    def __init__(self,**kwargs):
        super(Mahalanobis_Distance,self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight("kernel",
                                  shape=[input_shape[0][-1],input_shape[0][-1]])

    def call(self,inputs,**kwargs):
        support,query = inputs
        support = tf.matmul(support,self.kernel)
        query = tf.matmul(query,self.kernel)
        q2 = tf.reduce_sum(query ** 2, axis=1, keepdims=True)
        s2 = tf.reduce_sum(support ** 2, axis=1, keepdims=True)
        qdots = tf.matmul(query, support,transpose_b=True)
        return  -(tf.sqrt(q2 + tf.transpose(s2) - 2 * qdots))
    
    def compute_output_shape(self,input_shape):
        return tf.TensorShape(input_shape[:-1])

    def get_config(self):
        config = super(Mahalanobis_Distance,self).get_config()
        return config