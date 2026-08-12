import os
import glob
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestKriEitAgents(unittest.TestCase):

    def test_claude_agent_configs_exist(self):
        agents = glob.glob(os.path.join(REPO_ROOT, ".claude", "agents", "*.md"))
        self.assertEqual(len(agents), 6, f"Se esperaban 6 configuraciones de agente en .claude/agents/, se encontraron {len(agents)}")

    def test_claude_agent_yaml_frontmatter(self):
        agents = glob.glob(os.path.join(REPO_ROOT, ".claude", "agents", "*.md"))
        for agent_path in agents:
            with open(agent_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertTrue(content.startswith("---"), f"Falta YAML frontmatter en {os.path.basename(agent_path)}")
            self.assertIn("name:", content, f"Falta campo 'name' en {os.path.basename(agent_path)}")
            self.assertIn("description:", content, f"Falta campo 'description' en {os.path.basename(agent_path)}")
            self.assertIn("tools:", content, f"Falta campo 'tools' en {os.path.basename(agent_path)}")

    def test_prompt_files_xml_structure(self):
        prompts = glob.glob(os.path.join(REPO_ROOT, "asistente-*", "PROMPT.md"))
        self.assertEqual(len(prompts), 6, f"Se esperaban 6 PROMPT.md, se encontraron {len(prompts)}")
        required_tags = ["<agent>", "<role>", "<context>", "<workflow>", "<validation_checks>", "<constraints>"]

        for prompt_path in prompts:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            for tag in required_tags:
                self.assertIn(tag, content, f"Etiqueta XML requerida '{tag}' no encontrada en {prompt_path}")

    def test_test_suite_references_valid_agents(self):
        test_suite_path = os.path.join(REPO_ROOT, "TEST_SUITE.md")
        self.assertTrue(os.path.exists(test_suite_path), "TEST_SUITE.md no existe")

        with open(test_suite_path, 'r', encoding='utf-8') as f:
            content = f.read()

        expected_agents = ["@kri-ai", "@clainte", "@gain", "@laier", "@admain", "@visuai"]
        for agent in expected_agents:
            self.assertIn(agent, content, f"El agente '{agent}' no está referenciado en TEST_SUITE.md")

if __name__ == '__main__':
    unittest.main()
