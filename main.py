import streamlit as st
import sympy as sp
import plotly.graph_objs as go
import numpy as np

def parse_function(func_str):
    """Parse the input function string into a SymPy expression."""
    x = sp.Symbol('x')
    return sp.sympify(func_str)

def integrate_function(func, lower_bound, upper_bound):
    """Integrate the function symbolically and return the result."""
    x = sp.Symbol('x')
    integral = sp.integrate(func, x)
    result = integral.subs(x, upper_bound) - integral.subs(x, lower_bound)
    return integral, result

def plot_functions(func, integral, lower_bound, upper_bound):
    """Create a Plotly figure with the original function and its integral."""
    x = np.linspace(lower_bound, upper_bound, 1000)
    
    # Convert SymPy expressions to lambda functions
    f = sp.lambdify('x', func, 'numpy')
    F = sp.lambdify('x', integral, 'numpy')
    
    # Create traces for original function and integral
    trace_func = go.Scatter(x=x, y=f(x), mode='lines', name='Original Function')
    trace_integral = go.Scatter(x=x, y=F(x), mode='lines', name='Integral')
    
    # Create the layout
    layout = go.Layout(
        title='Function and its Integral',
        xaxis_title='x',
        yaxis_title='y',
        legend_title='Functions',
        hovermode='closest'
    )
    
    # Create the figure and return it
    fig = go.Figure(data=[trace_func, trace_integral], layout=layout)
    return fig

def main():
    st.title("Mathematical Integral Visualizer")
    
    st.write("""
    This app allows you to visualize mathematical integrals. Enter a function, 
    specify the range of integration, and see the result along with a graph.
    """)
    
    # User input for the function
    func_str = st.text_input("Enter a function of x (e.g., x**2 + 2*x + 1):", "x**2")
    
    # User input for integration range
    col1, col2 = st.columns(2)
    with col1:
        lower_bound = st.number_input("Lower bound of integration:", value=-5.0)
    with col2:
        upper_bound = st.number_input("Upper bound of integration:", value=5.0)
    
    try:
        # Parse the function and compute the integral
        func = parse_function(func_str)
        integral, result = integrate_function(func, lower_bound, upper_bound)
        
        # Display the results
        st.subheader("Results:")
        st.write(f"Original function: {sp.latex(func)}")
        st.write(f"Integral: {sp.latex(integral)} + C")
        st.write(f"Definite integral from {lower_bound} to {upper_bound}: {result.evalf()}")
        
        # Create and display the plot
        fig = plot_functions(func, integral, lower_bound, upper_bound)
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please check your input and try again.")

if __name__ == "__main__":
    main()
