import tensorflow as tf
from tensorflow import keras

class Euclidean_Distance(keras.layers.Layer):
    def __init__(self,**kwargs):
        super(Euclidean_Distance,self).__init__(**kwargs)
        #self.constant = tf.Variable(initial_value=0.1, dtype=tf.float32, trainable=True)

    def call(self,inputs,**kwargs):
        support,query = inputs
        q2 = tf.reduce_sum(query ** 2, axis=1, keepdims=True)
        s2 = tf.reduce_sum(support ** 2, axis=1, keepdims=True)
        qdots = tf.matmul(query, tf.transpose(support))
        return  -(tf.sqrt(q2 + tf.transpose(s2) - 2 * qdots))
    
    def compute_output_shape(self,input_shape):
        return tf.TensorShape(input_shape[:-1])
    
    def get_config(self):
        config = super(Euclidean_Distance,self).get_config()
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
        return  -((q2 + tf.transpose(s2) - 2 * qdots))
    
    def compute_output_shape(self,input_shape):
        return tf.TensorShape(input_shape[:-1])

    def get_config(self):
        config = super(Mahalanobis_Distance,self).get_config()
        return config


class Weighted_Euclidean_Distance(keras.layers.Layer):
    def __init__(self,**kwargs):
        super(Weighted_Euclidean_Distance,self).__init__(**kwargs)
        self.alpha = tf.Variable(
            initial_value=1.0, dtype=tf.float32, trainable=True)

    def call(self,inputs,**kwargs):
        support,query = inputs
        q2 = tf.reduce_sum(query ** 2, axis=1, keepdims=True)
        s2 = tf.reduce_sum(support ** 2, axis=1, keepdims=True)
        qdots = tf.matmul(query, tf.transpose(support))
        return  -(self.alpha * (q2 + tf.transpose(s2) - 2 * qdots))
    
    def compute_output_shape(self,input_shape):
        return tf.TensorShape(input_shape[:-1])
    
    def get_config(self):
        config = super(Weighted_Euclidean_Distance,self).get_config()
        return config

class New_Euclidean_Distance(keras.layers.Layer):
    def __init__(self,**kwargs):
        super(New_Euclidean_Distance,self).__init__(**kwargs)
        

    def build(self, input_shape):
        self.kernel = self.add_weight(
            "kernel",shape=[1,input_shape[0][-1]],
            initializer=tf.keras.initializers.Ones())

    def call(self,inputs,**kwargs):
        support,query = inputs
        support = support * self.kernel
        q2 = tf.reduce_sum(query ** 2, axis=1, keepdims=True)
        s2 = tf.reduce_sum(support ** 2, axis=1, keepdims=True)
        qdots = tf.matmul(query, tf.transpose(support))
        return  -(q2 + tf.transpose(s2) - 2 * qdots)
    
    def compute_output_shape(self,input_shape):
        return tf.TensorShape(input_shape[:-1])
    
    def get_config(self):
        config = super(New_Euclidean_Distance,self).get_config()
        return config