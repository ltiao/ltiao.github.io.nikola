.. title: Notes: Chapter 3, Pattern Recognition and Machine Learning (Bishop, C. M. 2007)
.. slug: notes-chapter-3-pattern-recognition-and-machine-learning-bishop-c-m-2007
.. date: 2015-10-28 16:31:44 UTC+11:00
.. tags: mathjax, machine learning, linear algebra, algebra, gradients
.. category: 
.. link: 
.. description: 
.. type: text

Equation 3.13
-------------

The gradient of the log-likelihood function is given in equation 3.13:

.. math::

   \nabla_{\mathbf{w}} \ln p(\mathbf{t} \mid \mathbf{w}, \beta) 
   = \beta \sum_{n=1}^N \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \} \phi(\mathbf{x}_n)^T

We derive this step-by-step below. First, the log-likelihood function is given 
by equation 3.11 and reproduced below,

.. math::

   \ln p(\mathbf{t} \mid \mathbf{w}, \beta) 
   &= \sum_{n=1}^N \ln \mathcal{N}(t_n \mid \mathbf{w}^T \phi(\mathbf{x}_n), \beta^{-1}) \\
   &= \frac{N}{2} \ln \beta - \frac{N}{2} \ln 2 \pi - \beta E_D(\mathbf{w})

where the sum-of-squares error function is given by equation 3.12,

.. math::

   E_D(\mathbf{w}) = \frac{1}{2} \sum_{n=1}^N \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \}^2

Then :math:`\nabla_{\mathbf{w}} \ln p(\mathbf{t} \mid \mathbf{w}, \beta)`, the 
gradient of the log-likelihood function *with respect to* :math:`\mathbf{w}` [#]_
is given by,

.. math::

   \nabla_{\mathbf{w}} \ln p(\mathbf{t} \mid \mathbf{w}, \beta) = - \beta \nabla_{\mathbf{w}} E_D(\mathbf{w})

where

.. math::

   \nabla_{\mathbf{w}} E_D
   = \begin{bmatrix} 
       \frac{\partial E_D}{\partial w_0} \\ 
       \vdots \\  
       \frac{\partial E_D}{\partial w_{M-1}} 
     \end{bmatrix}

and

.. math::

   \frac{\partial E_D}{\partial w_k} 
   &= \frac{\partial}{\partial w_k} \frac{1}{2} \sum_{n=1}^N \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \}^2 \\
   &= \frac{1}{2} \sum_{n=1}^N \frac{\partial}{\partial w_k} \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \}^2 \\

Since

.. math::

   \frac{\partial}{\partial w_k} \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \}^2
   = 2 \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \} \frac{\partial}{\partial w_k} \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \}

and

.. math::

   \frac{\partial}{\partial w_k} \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \}
   &= - \frac{\partial}{\partial w_k} \mathbf{w}^T \phi(\mathbf{x}_n) \\
   &= - \frac{\partial}{\partial w_k} \sum_{j=0}^{M-1} w_j \phi_j(\mathbf{x}_n) \\
   &= - \phi_k(\mathbf{x}_n)

we have

.. math::

   \frac{\partial}{\partial w_k} \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \}^2
   = - 2 \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \} \phi_k(\mathbf{x}_n)

and therefore

.. math::

   \frac{\partial E_D}{\partial w_k}  
   &= \frac{1}{2} \sum_{n=1}^N \frac{\partial}{\partial w_k} \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \}^2 \\
   &= - \sum_{n=1}^N \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \} \phi_k(\mathbf{x}_n) \\

Finally, we have

.. math::

   \nabla_{\mathbf{w}} E_D
   &= \begin{bmatrix} 
        \frac{\partial E_D}{\partial w_0} \\ 
        \vdots \\  
        \frac{\partial E_D}{\partial w_{M-1}} 
      \end{bmatrix} \\
   &= - \sum_{n=1}^N \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \} 
      \begin{bmatrix} 
        \phi_0(\mathbf{x}_n) \\ 
        \vdots \\  
        \phi_{M-1}(\mathbf{x}_n) 
      \end{bmatrix} \\
   &= - \sum_{n=1}^N \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \} \phi(\mathbf{x}_n)

and

.. math::

   \nabla_{\mathbf{w}} \ln p(\mathbf{t} \mid \mathbf{w}, \beta) 
   = \beta \sum_{n=1}^N \{ t_n - \mathbf{w}^T \phi(\mathbf{x}_n) \} \phi(\mathbf{x}_n)

Note that the final :math:`\phi(\mathbf{x}_n)` in equation 3.13 is given as 
its transpose, so that :math:`\nabla_{\mathbf{w}} \ln p(\mathbf{t} \mid \mathbf{w}, \beta)`
is a row vector. This was probably done to ease the derivation of the analytic 
solution which following immediately in the section. The only thing we need to 
alter in our derivation to make the result consistent with that of the book is 
to rewrite :math:`\nabla_{\mathbf{w}} E_D` as a row vector,

.. math::

   \nabla_{\mathbf{w}} E_D
   = \begin{bmatrix} 
       \frac{\partial E_D}{\partial w_0} & \cdots & \frac{\partial E_D}{\partial w_{M-1}} 
     \end{bmatrix}

.. [#] Since there is little possibility of confusion, the book omits the 
       subscript and simply writes :math:`\nabla` to denote the gradient w.r.t.
       :math:`\mathbf{w}`.

Equation 3.21
-------------

.. math::

   \ln p(\mathbf{t} \mid \mathbf{w}, \beta) 
   &= \frac{N}{2} \ln \beta - \frac{N}{2} \ln 2 \pi - \beta E_D(\mathbf{w}) \\
   \frac{\partial}{\partial \beta} \ln p(\mathbf{t} \mid \mathbf{w}, \beta) 
   &= \frac{N}{2 \beta} - E_D(\mathbf{w})

