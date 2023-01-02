#version 330 core

layout (location = 0) out vec4 frag_color;

in vec2 uv;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 ambient_intensity;
    vec3 diffuse_intensity;
    vec3 specular_intensity;
};

uniform Light light;
uniform vec3 camPos;

vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);

    // ambient light
    vec3 ambient = light.ambient_intensity;

    // diffuse light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.diffuse_intensity;

    // specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.specular_intensity;

    return color * (ambient + diffuse + specular);
}

void main () {
    vec3 color = vec3(1.0, 0.0, 0.0);
    color = getLight(color);
    frag_color = vec4(color, 1.0);
}