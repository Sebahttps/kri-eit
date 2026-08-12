import os
import glob
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestKriEitAgents(unittest.TestCase):

    def test_claude_agent_configs_exist(self):
        """Valida que existan al menos los agentes principales en .claude/agents/."""
        agents = glob.glob(os.path.join(REPO_ROOT, ".claude", "agents", "*.md"))
        self.assertGreaterEqual(len(agents), 6, f"Se esperaban al menos 6 configuraciones de agente en .claude/agents/, se encontraron {len(agents)}")

    def test_claude_agent_yaml_frontmatter(self):
        """Valida que todos los archivos en .claude/agents tengan el frontmatter YAML requerido."""
        agents = glob.glob(os.path.join(REPO_ROOT, ".claude", "agents", "*.md"))
        for agent_path in agents:
            with open(agent_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertTrue(content.startswith("---"), f"Falta YAML frontmatter en {os.path.basename(agent_path)}")
            self.assertIn("name:", content, f"Falta campo 'name' en {os.path.basename(agent_path)}")
            self.assertIn("description:", content, f"Falta campo 'description' en {os.path.basename(agent_path)}")

    def test_prompt_files_xml_structure(self):
        """Valida la presencia de estructura en cada PROMPT.md existente."""
        prompts = glob.glob(os.path.join(REPO_ROOT, "asistente-*", "PROMPT.md"))
        self.assertGreaterEqual(len(prompts), 6, f"Se esperaban al menos 6 PROMPT.md, se encontraron {len(prompts)}")

        for prompt_path in prompts:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertTrue("<agent>" in content or "<role>" in content or "<validation_checks>" in content,
                            f"Estructura de prompt no encontrada en {prompt_path}")

    def test_test_suite_exists(self):
        """Garantiza la existencia de TEST_SUITE.md."""
        test_suite_path = os.path.join(REPO_ROOT, "TEST_SUITE.md")
        self.assertTrue(os.path.exists(test_suite_path), "TEST_SUITE.md no existe")

if __name__ == '__main__':
    unittest.main()
