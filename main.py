import streamlit as st
import numpy as np
import plotly.graph_objects as go

def create_miura_ori(size=1.0, angle=45):
    """Create Miura-ori pattern unit cell"""
    # Convert angle to radians
    theta = np.radians(angle)
    
    # Basic parameters
    a = size  # length
    b = size  # width
    h = size/2  # height
    
    # Create vertices for one unit
    vertices = np.array([
        [0, 0, 0],
        [a*np.cos(theta), 0, a*np.sin(theta)],
        [a*np.cos(theta), b, a*np.sin(theta)],
        [0, b, 0],
        [2*a*np.cos(theta), 0, 0],
        [2*a*np.cos(theta), b, 0]
    ])
    
    # Define faces
    faces = [
        [0, 1, 2, 3],  # First parallelogram
        [1, 4, 5, 2]   # Second parallelogram
    ]
    
    # Define valley and mountain folds
    mountain_folds = [[1, 2]]  # Central fold
    valley_folds = [[0, 1], [2, 3], [1, 4], [2, 5]]  # Edge folds
    
    return vertices, faces, mountain_folds, valley_folds

def create_waterbomb(size=1.0):
    """Create Waterbomb pattern unit cell"""
    vertices = np.array([
        [0, 0, 0],  # Center
        [size, 0, 0],  # Right
        [size*np.cos(np.pi/3), size*np.sin(np.pi/3), 0],  # Upper right
        [-size*np.cos(np.pi/3), size*np.sin(np.pi/3), 0],  # Upper left
        [-size, 0, 0],  # Left
        [-size*np.cos(np.pi/3), -size*np.sin(np.pi/3), 0],  # Lower left
        [size*np.cos(np.pi/3), -size*np.sin(np.pi/3), 0]   # Lower right
    ])
    
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 5],
        [0, 5, 6],
        [0, 6, 1]
    ]
    
    mountain_folds = [[0, 2], [0, 4], [0, 6]]
    valley_folds = [[0, 1], [0, 3], [0, 5]]
    
    return vertices, faces, mountain_folds, valley_folds

def create_yoshimura(size=1.0, num_segments=6):
    """Create Yoshimura pattern unit cell"""
    vertices = []
    angle = 2 * np.pi / num_segments
    height = size/2
    
    # Create vertices
    for i in range(num_segments):
        theta = i * angle
        vertices.append([size * np.cos(theta), size * np.sin(theta), 0])
        vertices.append([size * np.cos(theta), size * np.sin(theta), height])
    
    vertices = np.array(vertices)
    
    # Create faces
    faces = []
    for i in range(num_segments):
        i1 = 2*i
        i2 = 2*i + 1
        i3 = 2*((i+1)%num_segments)
        i4 = 2*((i+1)%num_segments) + 1
        faces.append([i1, i2, i4, i3])
    
    mountain_folds = []
    valley_folds = []
    for i in range(num_segments):
        if i % 2 == 0:
            mountain_folds.append([2*i, 2*i+1])
        else:
            valley_folds.append([2*i, 2*i+1])
    
    return vertices, faces, mountain_folds, valley_folds

def plot_origami_lattice(vertices, faces, mountain_folds, valley_folds, colorscale='Viridis'):
    """Create interactive 3D plot for origami structure"""
    fig = go.Figure()
    
    # Plot faces
    for face in faces:
        vertices_face = vertices[face]
        x = vertices_face[:, 0].tolist() + [vertices_face[0, 0]]
        y = vertices_face[:, 1].tolist() + [vertices_face[0, 1]]
        z = vertices_face[:, 2].tolist() + [vertices_face[0, 2]]
        
        fig.add_trace(go.Mesh3d(
            x=vertices_face[:, 0],
            y=vertices_face[:, 1],
            z=vertices_face[:, 2],
            i=[0]*(len(face)-2),
            j=list(range(1, len(face)-1)),
            k=list(range(2, len(face))),
            opacity=0.7,
            colorscale=colorscale
        ))
    
    # Plot mountain folds
    for fold in mountain_folds:
        fig.add_trace(go.Scatter3d(
            x=[vertices[fold[0], 0], vertices[fold[1], 0]],
            y=[vertices[fold[0], 1], vertices[fold[1], 1]],
            z=[vertices[fold[0], 2], vertices[fold[1], 2]],
            mode='lines',
            line=dict(color='red', width=4),
            name='Mountain fold'
        ))
    
    # Plot valley folds
    for fold in valley_folds:
        fig.add_trace(go.Scatter3d(
            x=[vertices[fold[0], 0], vertices[fold[1], 0]],
            y=[vertices[fold[0], 1], vertices[fold[1], 1]],
            z=[vertices[fold[0], 2], vertices[fold[1], 2]],
            mode='lines',
            line=dict(color='blue', width=4, dash='dash'),
            name='Valley fold'
        ))
    
    fig.update_layout(
        scene=dict(
            aspectmode='cube',
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        showlegend=True,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

# Streamlit app
st.set_page_config(layout="wide", page_title="Origami Lattice Visualizer")
st.title("Origami-based Lattice Structure Visualizer")

# Create two columns
col1, col2 = st.columns([1, 3])

# Control panel
with col1:
    st.header("Settings")
    
    with st.expander("Pattern Settings", expanded=True):
        pattern_type = st.selectbox(
            "Select Origami Pattern",
            ["Miura-ori", "Waterbomb", "Yoshimura"]
        )
        
        size = st.slider("Unit Size", 0.5, 2.0, 1.0, 0.1)
        
        if pattern_type == "Miura-ori":
            angle = st.slider("Fold Angle", 30, 60, 45)
        elif pattern_type == "Yoshimura":
            segments = st.slider("Number of Segments", 4, 12, 6)
    
    with st.expander("Visualization Settings", expanded=True):
        colorscale = st.selectbox(
            "Color Scheme",
            ['Viridis', 'Plasma', 'Inferno', 'Magma', 'Rainbow']
        )

# Visualization area
with col2:
    if pattern_type == "Miura-ori":
        vertices, faces, mountain_folds, valley_folds = create_miura_ori(size, angle)
    elif pattern_type == "Waterbomb":
        vertices, faces, mountain_folds, valley_folds = create_waterbomb(size)
    else:  # Yoshimura
        vertices, faces, mountain_folds, valley_folds = create_yoshimura(size, segments)
    
    fig = plot_origami_lattice(vertices, faces, mountain_folds, valley_folds, colorscale)
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        ### How to Use
        1. Select origami pattern type
        2. Adjust pattern-specific parameters:
           - Unit size
           - Fold angles
           - Number of segments (for Yoshimura)
        3. Choose visualization settings
        
        ### Pattern Types
        - **Miura-ori**: Parallelogram-based folding pattern
        - **Waterbomb**: Radially symmetric pattern
        - **Yoshimura**: Diamond pattern with curved folding
        
        ### Fold Types
        - Red solid lines: Mountain folds
        - Blue dashed lines: Valley folds
        
        ### Interaction
        - Rotate: Click and drag
        - Zoom: Scroll
        - Pan: Right-click and drag
        """)

# Footer
st.markdown("---")
st.markdown("Created for visualization of origami-based lattice structures")
